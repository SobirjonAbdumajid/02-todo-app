from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:onamotam@localhost/todoapplicationdatabase'

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:sobirjonA1@127.0.0.1:3306/todoapplicationdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})  # connect_args is for detecting more database errors but in default we can get a error only

# engine = create_engine(SQLALCHEMY_DATABASE_URL)  # connect_args is for detecting more database errors but in default we can get a error only

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # if these are not False - autocommit=False, autoflush=False - aur database may try do somthing authomaticly

Base = declarative_base()  # we may controller database by using this
