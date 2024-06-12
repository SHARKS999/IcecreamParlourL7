Welcome to this python project


TITLE: ICECREAM  PARLOUR APPLICATION 

DESCRIPTION:

--> This application can be used to view the flavors that are already given using the SQLite database and add it to the cart with the allergies for that particular icecream 
--> This application can also be used to suggest some new flavors in the view flavors menu so that we can add new flavors in the future to our cart

To run this Project:

->Clone this project in your terminal -->
->Download the docker file that is uploaded and run it in your terminal using the following commands

-->docker build -t icecream-parlor-app .
after successful building of the application ,you have to download a X-server for viewing a GUI based application using docker that is Xming is used for my project which is easy to download and setup and after that run the following command in terminal

-->docker run -it --rm -e DISPLAY=host.docker.internal:0 -v C:/tmp/.X11-unix:/tmp/.X11-unix -v images:/app/images icecream-parlor-app

images:/app/images-->if this did not work change this path to the images path

If this command shows any error after running in the terminal, please create a file in the xming directory called  'X0.hosts' in that file give localhost and save it and then run the same command and it should run.

