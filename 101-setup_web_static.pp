# sets up a web server for the deployment of web_static.

package { 'update':
  ensure   => latest,
  provider => apt-get,
}

package { 'nginx':
  ensure   => present,
  provider => apt-get,
  require  => Package['update'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  recurse => true,
}

file { '/data/web_static/releases/test':
  ensure  => directory,
  recurse => true,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  require => File['/data/web_static/releases/test'],
}

exec { 'create_link':
  command  => 'ln -sf /data/web_static/releases/test /data/web_static/current',
  provider => shell,
  require  => File['/data/web_static/releases/test'],
}

exec { 'change_owner':
  command  => 'sudo chown -Rh ubuntu:ubuntu /data',
  provider => shell,
  require  => File['/data'],
}

exec { 'add_config':
  command  => 'sed -i ' +
  '"/server_name _;/ a \ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}"' +
  ' /etc/nginx/sites-available/default',
  provider => shell,
  require  => Package['nginx'],
}

service { 'nginx':
  ensure => running,
}
