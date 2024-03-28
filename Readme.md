# CSEDU Course-3111: Computer Networking Lab

This repository exists for the sole purpose of collaborating in team lab tasks. Feel free to use it for learning purposes. Some of the tasks might not be complete. So don't just copy them

## Table of Content
  - Lab 1 : [An Exercise on LAN Configuration and Troubleshooting Tools](https://github.com/ignite312/Networking-Lab/tree/main/Lab%201)
  - Lab 2 : [Introduction to Client-Server Communication using Socket Programming Machine Operation](https://github.com/ignite312/Networking-Lab/tree/main/Lab%202)
  - Lab 3 : [Implementing File transfer using SocketProgramming and HTTP GET/POST requests](https://github.com/ignite312/Networking-Lab/tree/main/Lab%203)
  - Lab 4 : [Distributed Database Management, Implementation of Iterative, and Recursive Queries of DNS Records](https://github.com/ignite312/Networking-Lab/tree/main/Lab%204)
  - Lab 5 : [Implementation of flow control and reliable data transfer through management of timeout, fast retransmit, cumulative acknowledgment, loss of data and acknowledgment packets.](https://github.com/ignite312/Networking-Lab/tree/main/Lab%205)
  - Lab 7 : [Implementation of Link State Routing Algorithm](https://github.com/ignite312/Networking-Lab/tree/main/Lab%207)
## Languages
 - ``Python`` ``v3.12.2``
 - ``LaTeX`` ``MiKTeX Utility v1.9 (MiKTeX v24.1)``

## Run Code
First open the directory of your server and client file
- Open Terminal
- Run command
```bash
python Server.py
```
- Run
```bash
python Client.py
```
- Or if a `main.py` file exists
```bash
python main.py
```
- If many server or client exists, run them each sperately in a terminal
```bash
python filename.py
```

 ## Find Your IP address
 For communication among different machines you need to put 
 ```Python
 HOST_IP = "YOUR_DEVICE_IP"
 ```
 To get your device IP, open terminal and run
 - Linux ``bash``
 ```bash
 hostname -I
 ```
 - Mac ``zsh``
 ```zsh
 ipconfig getifaddr en0
 ```
 - Windows ``cmd`` or ``ps``
 ```zsh
 ipconfig
 ```
 - For same device communication
 ```Python
 HOST_IP = socket.gethostbyname(socket.gethostname())
 ```
 or simply
 ```Python
 HOST_IP = "localhost"
 ```

 ## Render Latex Code

 - Install any latex renderer like [MikTeX](https://miktex.org/), or [LyX](https://www.lyx.org/), or anything else
 - Install [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) extension on VSCode
 - Or use [Overleaf](https://www.overleaf.com/). Also provides online collaboration

 ## Team
 - Md Emon Khan
 - Mahmudul Hasan