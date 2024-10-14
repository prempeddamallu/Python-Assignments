CREATE OR REPLACE PROCEDURE ManageEmployeeAndDepartment(
    EmployeeID INT,
    FirstName STRING DEFAULT NULL,
    LastName STRING DEFAULT NULL,
    Salary DECIMAL(10, 2) DEFAULT NULL,
    DepartmentID INT DEFAULT NULL,
    NewEmployeeID INT DEFAULT NULL,
    NewFirstName STRING DEFAULT NULL,
    NewLastName STRING DEFAULT NULL,
    NewSalary DECIMAL(10, 2) DEFAULT NULL,
    NewDepartmentID INT DEFAULT NULL,
    DepartmentName STRING DEFAULT NULL
)
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
    var result = "";
    
    // CREATE tables if not exist
    var createEmployeeTable = `CREATE TABLE IF NOT EXISTS Employee (
        EmployeeID INT PRIMARY KEY,
        FirstName STRING,
        LastName STRING,
        Salary DECIMAL(10, 2)
    )`;
    snowflake.execute({sqlText: createEmployeeTable});
    
    var createDepartmentTable = `CREATE TABLE IF NOT EXISTS Department (
        DepartmentID INT PRIMARY KEY,
        DepartmentName STRING
    )`;
    snowflake.execute({sqlText: createDepartmentTable});

    var createEmployeeDepartmentTable = `CREATE TABLE IF NOT EXISTS EmployeeDepartment (
        EmployeeID INT,
        DepartmentID INT,
        PRIMARY KEY (EmployeeID, DepartmentID),
        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
    )`;
    snowflake.execute({sqlText: createEmployeeDepartmentTable});

    result += "Tables created or already exist. ";

    // INSERT with JOIN (Insert into EmployeeDepartment from Employee and Department)
    if (NewEmployeeID !== null && NewDepartmentID !== null) {
        var insertEmployeeDepartmentStmt = `INSERT INTO EmployeeDepartment (EmployeeID, DepartmentID)
                                            SELECT e.EmployeeID, d.DepartmentID
                                            FROM Employee e
                                            JOIN Department d ON d.DepartmentID = ${NewDepartmentID}
                                            WHERE e.EmployeeID = ${NewEmployeeID}`;
        snowflake.execute({sqlText: insertEmployeeDepartmentStmt});
        result += "Record inserted into EmployeeDepartment with JOIN. ";
    }

    // UPDATE with JOIN (Update Employee's salary based on department)
    if (EmployeeID !== null && DepartmentID !== null && Salary !== null) {
        var updateStmt = `UPDATE Employee e
                          SET e.Salary = ${Salary}
                          FROM Department d
                          JOIN EmployeeDepartment ed ON ed.DepartmentID = d.DepartmentID
                          WHERE e.EmployeeID = ed.EmployeeID
                          AND e.EmployeeID = ${EmployeeID}
                          AND d.DepartmentID = ${DepartmentID}`;
        snowflake.execute({sqlText: updateStmt});
        result += "Employee salary updated with JOIN. ";
    }

    // DELETE without JOIN
    if (EmployeeID !== null && (DepartmentID === null)) {
        var deleteStmt = `DELETE FROM Employee WHERE EmployeeID = ${EmployeeID}`;
        snowflake.execute({sqlText: deleteStmt});
        result += "Employee record deleted. ";
    }

    // MERGE EmployeeDepartment using a JOIN
    if (EmployeeID !== null && NewDepartmentID !== null) {
        var mergeEmployeeDepartmentStmt = `MERGE INTO EmployeeDepartment AS target
                                           USING (SELECT ${EmployeeID} AS EmployeeID, ${NewDepartmentID} AS DepartmentID) AS source
                                           ON (target.EmployeeID = source.EmployeeID AND target.DepartmentID = source.DepartmentID)
                                           WHEN MATCHED THEN
                                               UPDATE SET DepartmentID = source.DepartmentID
                                           WHEN NOT MATCHED THEN
                                               INSERT (EmployeeID, DepartmentID)
                                               VALUES (source.EmployeeID, source.DepartmentID)`;
        snowflake.execute({sqlText: mergeEmployeeDepartmentStmt});
        result += "EmployeeDepartment record merged. ";
    }

    return result;
$$;
