## Add user and group
- sudo useradd -U emc
- sudo passwd emc
      input password for emc "asd"
## Change user and build system
- su - emc
      input password "asd"
- set workspace
      mkdir -p ~/workspace
      mkdir -p ~/workspace/code
      cd ~/workspace/code
      git clone https://github.com/yanghaa/Plone5.git
      git checkout dev1.1
      git pull origin dev1.1
      git submodule init
      git submodule update
      cd ..
      git clone https://github.com/yanghaa/plone.app.locales.git
      cp plone.app.locales /path/to/temp
      rm -rf /plone.app.locales/.git

## EMC
- build
      mkdir -p /home/vagrant/Plone/env    #用户路径需要修改
      sudo virtualenv --no-site-packages /home/vagrant/Plone/env/   #路径依旧需要修改
      source /home/vagrant/Plone/env/bin/activate                   #激活virtualenv
      python bootstrap.py -c buildout_dev.cfg
      bin/buildout -Nv -c buildout_dev.cfg
- 进入系统，注意防火墙，建立系统，安装附加组件，建立目录结构，准备配置生产模式
- 修改deploy_haproxy.cg #115 #117 #118 替换掉url。
- 修改haproxy.cfg #23 user #26
- 修改base.cfg effective-user = plone
- 生产模式
      sudo dnf install httpd -y
      cd /etc/httpd/conf/
      mv httpd.conf httpd.conf.bak
      sudo wget https://raw.githubusercontent.com/adam18975257327/emc/master/httpd.conf
      sudo vim httpd.conf
      replace #97
      sudo /bin/systemctl start httpd.service
      sudo systemctl enable httpd.service
      修改deploy_haproxy.cg #115 #117 #118 替换掉url、修改haproxy.cfg #23 user、修改base.cfg effective-user = plone
      bin/buildout -Nv -c deploy_haproxy.cfg
