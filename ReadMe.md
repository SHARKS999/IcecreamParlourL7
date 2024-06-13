Welcome to this python project


TITLE: ICECREAM  PARLOUR APPLICATION 

DESCRIPTION:

--> This application can be used to view the flavors that are already given using the SQLite database and add it to the cart with the allergies for that particular icecream 
--> This application can also be used to suggest some new flavors in the view flavors menu so that we can add new flavors in the future to our cart

To run this Project:

 Method 1:

-->Clone this project in your terminal --> git clone https://github.com/SHARKS999/IcecreamParlourL7

--> In your virtual environment install docker package if not available using the following command in the terminal: pip install docker

--> Download the docker desktop on your system and setup it and after downloading verify whether the docker is successfully installed on tour system using the following command in the command prompt:  docker --version

-->Docker download link: https://docs.docker.com/desktop/install/windows-install/
 
->Download the docker file that is uploaded and run it in your terminal using the following commands

-->docker build -t icecream-parlor-app .

After successful building of the application ,you have to download a X-server for viewing a GUI based application using docker that is Xming is used for my project which is easy to download and setup and after that run the following command in terminal

--> Xming download link: https://sourceforge.net/projects/xming/   (After completing installation click once to activate the server)

-->docker run -it --rm -e DISPLAY=host.docker.internal:0 -v C:/tmp/.X11-unix:/tmp/.X11-unix -v images:/app/images icecream-parlor-app

images:/app/images-->if this did not work change this path to the images path

If this command shows any error after running in the terminal, please create a file in the xming directory called  'X0.hosts' in that file give localhost and save it and then run the same command and it should run.


Method 2:

-->Clone this project in your terminal --> git clone https://github.com/SHARKS999/IcecreamParlourL7

--> After cloning you can see a main.py file in the directory run that file to view the output.

