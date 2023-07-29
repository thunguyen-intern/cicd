FROM hikari141/odoo15:latest

#Install requirements
ADD /odoo.conf /etc/
ADD ./customized_addons /opt/odoo/customized_addons/
COPY /requirements.txt /
RUN sudo apt-get install python3.8-venv \
    && python3 -m venv env \
    && source env/bin/activate \
    && pip install --upgrade pip \
    && pip install wheel setuptools \
    && pip install -r /requirements.txt

RUN chmod +x /opt/odoo/odoo-bin \
    && mkdir -p /mnt/extras \
    && mkdir -p /mnt/source

RUN chmod 755 /mnt/extras

ADD ./unit_test/ /mnt/extras/

EXPOSE 8069 8071 8072

USER odoo

ENTRYPOINT ["/opt/odoo/odoo-bin"]
CMD ["-c", "/etc/odoo.conf"]