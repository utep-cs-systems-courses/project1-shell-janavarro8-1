#!/usr/bin/env python3

import os
import sys
import re

def main():
    while True:
        if 'PS1' in os.environ:
            os.write(1,(os.environ['PS1']).encode())
        else:
            os.write(1,(os.getcwd().split("/")[-1] + "$ ").encode())
        userInput = input()

        if userInput == "exit":
            break

        if userInput.startswith("cd ") and len(userInput) > 3:
            directory = userInput.split("cd")[1].strip()    #grabs directory given
            try:
                os.chdir(directory)
            except FileNotFoundError:
                os.write(1, ("cd: %s: No such file or directory\n" % directory).encode())
            continue

        elif userInput.startswith("ls"):
            directoryList = os.listdir(os.getcwd())
            for i in directoryList:
                print(i, end = " ")
            print("")

        elif userInput.startswith("ls > ") and len(userInput) > 5 and userInput.endswith(".txt"):
            slashes = userInput.split("/")
            directoryList = os.listdir(os.getcwd())
            for i in range(1, len(slashes) - 1):    #go through path
                try:
                    os.chdir(slashes[i])
                except FileNotFoundError:
                    os.write(1, ("cd: %s: No such file or directory\n" % directory).encode())
                continue
            fdOut = os.open(slashes[-1], os.O_CREAT | os.O_WRONLY)  #open file as write only
            for i in directoryList:     #write out directory list
                os.write(fdOut, (i+"\n").encode())
            for i in range(len(slashes)-2):    #go back to original directory
                os.chdir("..")

        elif (userInput.startswith("wc ") and len(userInput) > 3) or (userInput.startwith("python3 ") and len(userInput) > 8):
            rc = os.fork()

            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc == 0:
                if(userInput.startswith("wc")):
                    files = userInput.split("wc")[1].strip()
                    args = ["wc", files]
                else:
                    files = userInput.split("python3")[1].strip()
                    args = ["python3", files]
                for dir in resplit(":", os.environ['PATH']):    #try each directory in the path
                    program = "%s%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ)    #execute program
                    except FileNotFoundError:
                        pass
                os.write(2, ("Child: Could not exec %s\n" % args[0].encode()))
                sys.exit(1)     #terminate with error
            else:
               os.wait()


main()