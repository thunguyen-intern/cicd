FROM hikari141/odoo15:latest

#Install requirements
ADD /odoo.conf /etc/
ADD ./customized_addons /opt/odoo/customized_addons/
COPY /entrypoint.sh /
COPY /requirements.txt /
RUN pip install --upgrade pip \
    && pip install wheel setuptools \
    && pip install -r /requirements.txt

RUN chmod +x /entrypoint.sh \
    && chmod +x /opt/odoo/odoo-bin \
    && mkdir -p /mnt/extras \
    && mkdir -p /opt/odoo/unit_test

ADD ./odoo-ex-file /opt/odoo/unit_test/
RUN chmod 755 /opt/odoo/unit_test

EXPOSE 8069 8071 8072

USER odoo

WORKDIR /opt/odoo/unit_test

ENTRYPOINT []
# CMD ["-c", "/etc/odoo.conf"]