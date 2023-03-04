# Base on the most recently released Fedora
FROM fedora:latest
MAINTAINER prentrodgers email prent@ripnread.com

# Install updates and httpd
RUN echo "Updating all fedora packages"; dnf -y update; dnf -y clean all
RUN echo "Installing csound-devel"; dnf -y install csound-devel && dnf -y clean all

# Expose the default httpd port 80
# EXPOSE 80

# Run csound and pass some options.
CMD ["csound", "-DFOREGROUND"]