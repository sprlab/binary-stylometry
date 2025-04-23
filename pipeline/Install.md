## Installation Guide

This guide provides step-by-step instructions to install the third-part software required by the pipeline including **Joern, Neo4j, bjoern-radare2**, and related dependencies for the pipeline.  

## Prerequisites

- A **Linux-based system** (Ubuntu recommended)
- **Java Versions**:
  - Java 7for Neo4j
  - Java 11 for running the source Java files of the source files located in `Attribution/src` folder.

## Installation Steps

All these steps should be performed inside the `./pipeline` directory.

### 1. Install Dependencies

Ensure your system has all required packages installed:

```sh
sudo apt update
sudo apt install -y unzip ant wget openjdk-11-jdk python-setuptools python-dev python2-dev python2-pip git vim dpkg \
graphviz libgraphviz-dev pkg-config build-essential autoconf libtool libssl-dev libffi-dev libxml2-dev \
libxslt1-dev zlib1g-dev portaudio19-dev python3-dev python3-pip
```


### 2. Download and Build Joern

```sh
wget https://github.com/fabsx00/joern/archive/0.3.1.tar.gz
tar xfzv 0.3.1.tar.gz
cd joern-0.3.1
wget http://mlsec.org/joern/lib/lib.tar.gz
tar xfzv lib.tar.gz
ant
ant tools
echo "alias joern='java -jar $JOERN/bin/joern.jar'" >> ~/.bashrc
source ~/.bashrc
cd ..
```


### 3. Install Python Dependencies

```sh
wget https://pypi.python.org/packages/d0/5b/ce38fbd03cd645ab4f121e7df70964a8baeab5cbbabf22e9ed8abfa1aa17/py2neo-2.0.9.tar.gz
tar xfzv py2neo-2.0.9.tar.gz
cd py2neo-2.0.9
sudo python2 setup.py install
cd ..
```

### 4. Install Python Joern

```sh
git clone https://github.com/EdgeDauDrex/python-joern.git
cd python-joern
sudo python2 setup.py install
cd ..
```

### 5. Install Neo4j

```sh
wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install -y neo4j=2.1.5
```

Note: Neo4j requires manual configuration of `neo4j.conf` and `neo4j-server.properties` to set up the path of `.joernIndex` that is located in Attribution.


### 6. Configure Plugins

```sh
git clone https://github.com/EdgeDauDrex/CodeStylometry.git
git clone https://github.com/EdgeDauDrex/CodeStylometry-missing-joern-tools-files.git
mv CodeStylometry-missing-joern-tools-files/plugins/neo4j-gremlin-plugin-2.1-SNAPSHOT.jar /usr/share/neo4j/plugins/
mv CodeStylometry-missing-joern-tools-files/plugins/gremlin-plugin /usr/share/neo4j/plugins/
```

### 7. Install Joern Tools

```sh
sudo apt install -y graphviz libgraphviz-dev pkg-config
git clone https://github.com/fabsx00/joern-tools
cd joern-tools
sudo python setup.py install
cd ..
```

### 8. Install bjoern-radare2

Installation instructions are provided at the following link: https://bjoern.readthedocs.io/en/latest/installation.html

Ensure these files are in the folder bjoern-radare after installation:
- `bjoern-radare/bin/bjoern.jar`
- `bjoern-radare/bjoern-server.sh`


### 9. Setup for remaining Files

```sh
cd CodeStylometry-missing-joern-tools-files/
python2 template.py
cd ..
```

### 10. Install any python dependencies

```sh
pip3 install -r requirements.txt
```

**If you encounter any issues:**  
- Ensure all dependencies are installed correctly.
- If you still encounter an error, we have a docker file with all the tools installed and configured with the pipeline that we can provide you on demand.
