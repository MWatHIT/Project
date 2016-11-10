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
      
