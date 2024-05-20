# sets up a web server for the deployment of web_static.

$line = '\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}'

exec { 'update':
  command  => 'sudo apt-get update',
  path     => ['/usr/bin', '/usr/sbin'],
  provider => shell,
}

package { 'nginx':
  ensure  => present,
  require => Exec['update'],
}

exec { '/usr/bin/mkdir -p /data/web_static/shared':
  provider => shell,
}

exec { '/usr/bin/mkdir -p /data/web_static/releases/test':
  provider => shell,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>",
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
}

exec { 'ln -sfT /data/web_static/releases/test /data/web_static/current':
  path     => ['/usr/bin', '/usr/sbin'],
  provider => shell,
}

exec { 'sudo chown -Rh ubuntu:ubuntu /data':
  path     => ['/usr/bin', '/usr/sbin'],
  provider => shell,
}

exec { 'add_config':
  command  => "sed -i '/server_name _;/ a ${line}' /etc/nginx/sites-available/default",
  provider => shell,
  require  => Package['nginx'],
}

exec {'sudo service nginx restart':
  path     => ['/usr/bin', '/usr/sbin'],
  provider => shell,
}
