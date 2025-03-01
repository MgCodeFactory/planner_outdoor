CREATE DATABASE po_db CHARACTER SET utf8mb4;
CREATE DATABASE test_po_db CHARACTER SET utf8mb4;
CREATE USER 'po_admin'@'%' IDENTIFIED BY "replace_by_your_admin_password";
GRANT ALL PRIVILEGES ON po_db.* TO 'po_admin'@'%';
GRANT ALL PRIVILEGES ON test_po_db.* TO 'po_admin'@'%';
FLUSH PRIVILEGES;
