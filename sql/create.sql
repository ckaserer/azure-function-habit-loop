CREATE TABLE habits (
    ID int NOT NULL
            IDENTITY(1,1),
    habit text NOT NULL,
    occured bigint NOT NULL,
    PRIMARY KEY (ID)
);