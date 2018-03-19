Models = [
    """
    CREATE TABLE IF NOT EXISTS admin (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        account VARCHAR(30) NOT NULL,
        password VARCHAR(30) NOT NULL,
        username VARCHAR(30) NOT NULL,
        is_super TINYINT DEFAULT 0,
        create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS user (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        account VARCHAR(30) NOT NULL,
        password VARCHAR(30) NOT NULL,
        username VARCHAR(30) NOT NULL,
        education VARCHAR(30) NOT NULL,
        grade VARCHAR(30) NOT NULL,
        score INT DEFAULT 0,
        fund INT DEFAULT 0,
        telephone VARCHAR(30) DEFAULT '',
        qq VARCHAR(30) DEFAULT '',
        create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS scorelog (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        value INT NOT NULL,
        summary VARCHAR(30) NOT NULL,
        detail VARCHAR(200) NOT NULL,
        update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id),
        FOREIGN KEY(user_id) REFERENCES user(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS fundlog (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        value INT NOT NULL,
        summary VARCHAR(30) NOT NULL,
        detail VARCHAR(200) NOT NULL,
        update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id),
        FOREIGN KEY(user_id) REFERENCES user(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
]
