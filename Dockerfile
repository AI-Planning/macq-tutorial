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

# Copy examples.py into /usr/local/bin so it's publicly available
COPY examples.py /usr/local/bin/examples.py

# Create a script there to invoke it
RUN echo '#!/bin/bash' > /usr/local/bin/macq-tutorial
RUN echo 'python3 /usr/local/bin/examples.py' >> /usr/local/bin/macq-tutorial
RUN chmod +x /usr/local/bin/macq-tutorial


WORKDIR /root/work

CMD planutils activate
