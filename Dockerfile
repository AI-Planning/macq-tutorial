# Build the Planutils image and install the selected packages
FROM aiplanning/planutils:latest


RUN apt-get update && apt-get -y install locales
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get update && apt-get install --no-install-recommends -y \
    graphviz python-is-python3

# Needed for the server (useful for many of the modules with the vscode plugin)
RUN pip3 install --upgrade flask
RUN pip3 install --upgrade graphviz
RUN pip3 install --upgrade tqdm
RUN pip3 install --upgrade pygments


RUN planutils install -f -y lama-first
RUN planutils install -f -y lama
RUN planutils install -f -y macq


# Misc
RUN planutils install -f -y val

WORKDIR /root/macq-tutorial

CMD planutils activate
