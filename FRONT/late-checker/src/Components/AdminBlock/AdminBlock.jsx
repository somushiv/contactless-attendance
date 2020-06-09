import React, { useState } from "react";
import EmployeeDetails from "./EmployeeDetails";

const AdminBlock = () => {
  const [nameList, setNameList] = useState({});
  const [isEmployeeListLoaded, setIsEmployeeListLoaded] = useState(false);
  const [isEmpDetails, setIsEmpDetails] = useState(false);
  const [empDetails, setEmpDetails] = useState();
  const [selectedEmployee, setSelectedEmployee] = useState();
  //Data Table Spec

  const getEmployeeList = () => {
    fetch("http://127.0.0.1:5000/list_employee")
      .then((response) => response.json())
      .then((response) => {
        if (!isEmployeeListLoaded) {
          console.log(response);
          setNameList(response);
          setIsEmployeeListLoaded(true);
        }
      });
  };
  const onEmplooyeeChange = (e) => {
    setSelectedEmployee(e.target.value);
    const requestOption = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emp_number: e.target.value }),
    };
    fetch("http://127.0.0.1:5000/employee_data", requestOption)
      .then((response) => response.json())
      .then((response) => {
        console.log(response);
        setEmpDetails(response);
        setIsEmpDetails(true);
      });
  };
  return (
    <>
      <h2>Staff Management</h2>

      <button onClick={getEmployeeList}>Load Employee List</button>
      {isEmployeeListLoaded ? (
        <div className="row content-block">
          <div className="col-sm-12 col-md-4 ">
            <label>Select Employee</label>
          </div>
          <div className="col-sm-12 col-md-8">
            <select
              id="employees"
              onChange={onEmplooyeeChange}
              className="form-control"
            >
              {nameList.map((item, key) => (
                <option
                  key={item.emp_number}
                  dataid={item.emp_number}
                  value={item.emp_number}
                >
                  {item.emplyeename}
                </option>
              ))}
            </select>
            {isEmpDetails ? (
              <div className="row content-block ">
                <EmployeeDetails empDetails={empDetails} />
              </div>
            ) : (
              "Employee Details"
            )}
          </div>
        </div>
      ) : (
        "Not Loaded"
      )}
      {/* Employee Details  */}
    </>
  );
};

export default AdminBlock;
