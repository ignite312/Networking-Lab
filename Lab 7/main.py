import socket
import threading
import json
import time
import os
import multiprocessing
import heapq
import random
from collections import defaultdict

HOST = "localhost"
ENCODER = "utf-8"
BYTESIZE = 65536
routers = {}
TTL = 60
timer = 0

print_lock = threading.Lock()

def dijkstra(graph, source):
    edges = defaultdict(list)
    for edge in graph:
        src, dest, weight = edge
        edges[src].append((dest, weight))
        edges[dest].append((src, weight))  # Assuming the graph is undirected
    
    distances = {vertex: float("inf") for vertex in edges}
    distances[source] = 0

    pq = [(0, source)]

    while pq:
        dist, vertx = heapq.heappop(pq)

        if dist > distances[vertx]:
            continue

        for neigh, edge_wt in edges[vertx]:
            distance = dist + edge_wt
            if distance < distances[neigh]:
                distances[neigh] = distance
                heapq.heappush(pq, (distance, neigh))
    
    edges = [[min(source, d), max(source, d), distances[d]] for d in distances if d != source and distances[d] != float("inf")]
    return edges

def countDown(timer):
    # timer = 0
    while True:
        # print(timer)
        time.sleep(1)
        timer += 1
        if timer == 3600:
            return

def getTimeNow():
    return timer

def createRouters():
    data = {}
    with open("routerMapping.json", "r") as file:
        data = json.load(file)
    # print(json.dumps(data, indent=4))
    number_of_routers = len(data["routers"])

    for i in range(len(routers), number_of_routers):
        router_name = f"router{i+1}"
        port = data["routers"][router_name]
        address = (HOST, port)
        router_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        router_socket.bind(address)
        # router_socket.setblocking(0)
        router_socket.listen()
        # print(f"initiated router {router_name}: {address}")

        routers[router_name] = (address, router_socket)

    # print(json.dumps(routers, indent=4))

def getLinksFromGraph(name):
    data = {}
    with open("routerMapping.json", "r") as file:
        data = json.load(file)
    links = [[min(row[0], row[1]), max(row[0], row[1]), row[2]] for row in data["graph"] if name in row]
    return links

def printOptimumRoutes(name):
    print(f"Optimum Costs for {name}:")
    filename = "links/" + name + ".json"
    with open(filename, "r") as file:
        records = json.load(file)
        print([r for r in records[0]["links"] if name in r])

def sendLinks(name, recvdfrom, router_records):
    # print(router_records)
    message = json.dumps({
        "id": name,
        "ttl": TTL,
        "links": router_records
    }, indent=4)

    routerslist = set()
    for record in router_records:
        r1, r2, _ = record
        routerslist.add(r1)
        routerslist.add(r2)
    
    for router in routerslist:
        if router == name or router == recvdfrom:
            continue
        address, _ = routers[router]
        rlist = set()
        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect(address)
            sender_socket.sendall(message.encode(ENCODER))
        except ConnectionRefusedError:
            # print(f"All sorted out for {address}")
            _, port = address
            rlist.add(port)
            if len(rlist) == len(routerslist):
                sender_socket.close()
                break
        finally:
            sender_socket.close()

def saveUpdate(name, update):
    # print(update)
    filename = "links/" + name + ".json"
    writeable = []
    with open(filename, "r") as file:
        # print(file.read())
        writeable = json.load(file)
    
    writeable = [d for d in writeable if d["savetime"] + d["ttl"] < getTimeNow()]

    isUpdated = False
    for d in writeable:
        if d["id"] == update["id"]:
            d.update(update)
            isUpdated = True
            break
    if not isUpdated:
        writeable.append(update)
    writeable = sorted(writeable, key=lambda x: (x["id"]))
    with open(filename, "w") as file:
        file.write(json.dumps(writeable, indent=4))

def createGraph(name, mssg):
    filename = "links/" + name + ".json"
    savedrecords = []
    with open(filename, "r") as file:
        savedrecords = json.load(file)
    graph = []
    for record in savedrecords:
        graph.extend(record["links"])
    graph.extend(mssg["links"])
    graph = sorted(graph, key=lambda x: (x[0], x[1], x[1]))
    opt_graph = []
    prev_edge = ["prev0", "prev1", 0]
    for edge in graph:
        if edge[0] == prev_edge[0] and edge[1] == prev_edge[1]:
            prev_edge = edge
            continue
        opt_graph.append(edge)
        prev_edge = edge
    return opt_graph

def isEqual(list1, list2):
    if list1 == list2:
        return True
    if len(list1) == len(list2):
        ln = len(list1)
        for i in range(0, ln):
            return isEqual(list1[i], list2[i])
    return False

def handleUpdate(name, mssg):
    mssg = {
        "id": mssg["id"],
        "savetime": getTimeNow(),
        "ttl": mssg["ttl"],
        "links": mssg["links"]
    }
    graph = createGraph(name, mssg)
    # print("\n\n", name, graph, "\n\n")
    shortest_paths = dijkstra(graph, name)

    graph.extend(shortest_paths)
    graph = sorted(graph, key=lambda x: (x[0], x[1], x[2]))
    # print(f"\n\n{name}, shortest paths: {shortest_paths}\n\n")
    optimized_graph = []
    prev_edge = ["prev0", "prev1", 0]
    for edge in graph:
        if edge[0] == prev_edge[0] and edge[1] == prev_edge[1]:
            prev_edge = edge
            continue
        optimized_graph.append(edge)
        prev_edge = edge
    # print(optimized_graph, graph)
    modified = isEqual(sorted(optimized_graph), sorted(graph))
    # saveUpdate(name, mssg)
    saveLinks(name, optimized_graph)
    return modified, optimized_graph

def saveLinks(name, router_records):
    update = {
        "id": name,
        "savetime": getTimeNow(),
        "ttl": TTL,
        "links": sorted(router_records, key=lambda x: (x[0], x[1], x[2]))
    }
    saveUpdate(name, update)

def handlerouter(name, address, router_socket):
    # print(f"router Active {name}: {address}")

    # get initial links of this router
    router_records = getLinksFromGraph(name)
    saveLinks(name, router_records)
    # print(router_records)

    # wait till all routers/threads are active
    time.sleep(10)
    
    # send initial links
    sendLinks(name, "", router_records)

    while True:
        client_socket, client_address = router_socket.accept()
        mssg = client_socket.recv(BYTESIZE).decode(ENCODER)
        # client_socket.send("Got It".encode(ENCODER))
        client_socket.close()
        # print(json.loads(mssg))
        recvdmssg = json.loads(mssg)
        modified, optimized_graph = handleUpdate(name, recvdmssg)
        if modified:
            sendLinks(name, recvdmssg["id"], optimized_graph)
        # print(f"{name} received message from {client_address}: {mssg}\n\n")
        
def init():
    createRouters()
    threads = []
    i = 0
    threading.Thread(target=countDown, args=(timer,)).start()
    try:
        for router in routers:
            threads.append([])
            name = router
            address, router_socket = routers[router]
            threads[i] = threading.Thread(target=handlerouter, args=(name, address, router_socket,))
            threads[i].start()
            i += 1
    except KeyboardInterrupt:
        for router in routers:
            _, router_socket = routers[router]
            router_socket.close()
        for thread in threads:
            thread.join()
        print("Closed all threads")

def get_most_recent_update_time(directory):
    most_recent_time = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mod_time = os.path.getmtime(file_path)
            if mod_time > most_recent_time:
                most_recent_time = mod_time

    return most_recent_time

def generate_random_graph(n, m):
    routers = {f"router{i+1}": 8000 + i + 1 for i in range(n)}

    edges = []
    used_pairs = set()
    while len(edges) < m:
        router1 = random.randint(1, n)
        router2 = random.randint(1, n)
        if router1 >= router2:
            continue

        pair = (min(router1, router2), max(router1, router2))
        if pair in used_pairs:
            continue

        weight = random.randint(1, 100)

        edges.append([f"router{router1}", f"router{router2}", weight])
        used_pairs.add(pair)

    graph = {
        "routers": routers,
        "graph": edges
    }

    return graph

def delete_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception as e:
                pass

def create_router_files(directory, n):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        return

    for i in range(1, n + 1):
        file_name = os.path.join(directory, f"router{i}.json")
        try:
            with open(file_name, "w") as file:
                json.dump([], file)
        except IOError as e:
            pass

def extract_router_links(directory):
    result = {}

    for filename in os.listdir(directory):
        if filename.startswith("router") and filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    for item in data:
                        for row in item["links"]:
                            fname = filename.split(".")[0]
                            if fname in row:
                                if fname not in result.keys():
                                    result[fname] = []
                                result[fname].append([r for r in row if r != fname])

                    
            except (IOError, ValueError) as e:
                print(f"Error processing file {file_path}: {e}")

    return result

if __name__ == "__main__":

    analysis = []
    test_number = 1
    i = 2
    while i <= 1000:
        m = i
        while m <= (i * (i-1)) // 2:
            print(f"Test {test_number}: Running new test...\n")
            delete_files("links/")
            create_router_files("links/", i)
            graph = generate_random_graph(i, m)
            with open("routerMapping.json", "w") as file:
                file.write(json.dumps(graph, indent=4))

            process = multiprocessing.Process(target=init)

            start = time.time()
            process.start()
            time.sleep(40)
            process.terminate()

            end = get_most_recent_update_time("links/")

            result = extract_router_links("links/")
            elapsed_time = end-start-10

            with open("ExperimentReseults.txt", "a") as file:
                file.write(f"Test {test_number}: Running new test...\n")
                for key in result:
                    print(f"Router {key} shortest paths: {result[key]}")
                    file.write(f"Router {key} shortest paths: {result[key]}\n")
                print(f"Total nodes: {i}\tTotal links: {m}\tTime elapsed: {elapsed_time}\n")
                file.write(f"Total nodes: {i}\tTotal links: {m}\tTime elapsed: {elapsed_time}\n\n")
            
            elapsed_time = end-start-10
            

            analysis.append([i, m, elapsed_time])

            m *= 2
            test_number += 1
        i *= 2

    print("\n\nAll samples finished testing.\n Here's an analysis of the Link State algorightm implementation:\n\n")

    for a in analysis:
        n, m, elapsed = a
        print(f"Number of nodes: {n}")
        print(f"Number of edges: {m}")
        print(f"Total Time Taken by the Process: {elapsed}")
        print()
    # printOptimumCosts()