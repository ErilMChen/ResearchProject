myhost="dubbusdb.cayveqvorwmz.eu-west-1.rds.amazonaws.com"
mypasswd="t8dubbus"
myuser="admin"
mydatabase="dubbusdb"
mycharset="utf8mb4"

engine = f"mysql+mysqlconnector://{myuser}:{mypasswd}@{myhost}:3306/{mydatabase}"
