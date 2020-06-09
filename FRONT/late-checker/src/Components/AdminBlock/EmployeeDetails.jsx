import React from "react";
import { Link, useHistory, withRouter } from "react-router-dom";

function EmployeeDetails({ empDetails }) {
  let history = useHistory();
  console.log(empDetails.emp_number);
  const onEnrollClick = () => {
    localStorage.setItem("empDetails", JSON.stringify(empDetails));
    history.push("/staff_enrollment");
  };
  //   const onEnrollClick1 = () => {
  //     const emp = JSON.parse(localStorage.getItem("empDetails"));
  //     console.log(emp.city_code);
  //   };
  return (
    <div className="content-block">
      <h3>Employee Details</h3>
      <div className=" row ">
        <div className="col-sm-12 col-md-4">Full Name</div>
        <div className="col-sm-12 col-md-8">{empDetails.emplyeename}</div>
        <div className="col-sm-12 col-md-4">City</div>
        <div className="col-sm-12 col-md-8">{empDetails.city_code}</div>
        <div className="col-sm-12 col-md-4">DB.Ref.ID</div>
        <div className="col-sm-12 col-md-8">{empDetails.emp_number}</div>
        <div className="col-sm-12 text-center">
          <button className="btn btn-primary" onClick={onEnrollClick}>
            Enroll
          </button>
          {/* <button className="btn btn-primary" onClick={onEnrollClick1}>
            Enroll1
          </button> */}
        </div>
      </div>
    </div>
  );
}

export default EmployeeDetails;
