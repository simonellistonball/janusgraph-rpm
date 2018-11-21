# JanusGraph RPM

An RPM wrapper around JanusGraph binary release packages.

The RPM building Docker container is inspired by https://github.com/apache/metron/tree/master/metron-deployment/packaging/docker/rpm-docker

## Building

1. Download a JanusGraph release from https://github.com/JanusGraph/janusgraph/releases and put it in the releases folder.
2. Run `mvn clean package`
3. Copy the files in target/RPMS to a hosting location (this includes all yum repodata files already)

Note: if you want to maintain a history in your YUM repo, you will only want to copy the RPM and you will have to run createrepo yourself.