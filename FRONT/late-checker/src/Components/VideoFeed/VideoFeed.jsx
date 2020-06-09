import React, { useState, useRef } from "react";
import styled from "styled-components";
import "./videoStyle.css";
import Webcam from "react-webcam";
import DataVideoSet from "./DataVideoSet";

const videoConstraints = {
  facingMode: "user",
};

const VideoFeed = () => {
  // Get Employee Details

  const [empDetails, setEmpDetails] = useState(
    JSON.parse(localStorage.getItem("empDetails"))
  );
  const [parData, setParData] = useState("This is one its working");
  const numImages = ["imtma1", "imtma2", "imtma3"];
  const [dataset_images, setDataset_images] = useState(numImages);
  const VideoFeedSection = styled.section`
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    width: 45vw;
  `;

  const updateImageData = (img_parameter, img_reference) => {
    let tmp_array = dataset_images;
    tmp_array[img_parameter] = img_reference;
    setDataset_images(tmp_array);
    console.log(dataset_images);
  };
  const webcamRef = useRef(null);
  // const capture = React.useCallback(() => {
  //   const imageSrc = webcamRef.current.getScreenshot();
  //   console.log(imageSrc);
  //   setImgData(imageSrc);
  //   setimgPlaceHolder(<img src={imageSrc} id="profileImage" />);
  // }, [webcamRef]);

  const saveImage = () => {
    // const refImage = document.getElementById("somu1");
    // var imgData = refImage.src;
    fetch("http://127.0.0.1:5000/saveimage", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image_data: dataset_images,
        emp_number: empDetails.emp_number,
      }),
    })
      .then((reposonse) => reposonse.json())
      .then((response) => {
        console.log(response);
      });
  };

  return (
    <>
      <h2>
        Registration for {empDetails.emplyeename} , # {empDetails.emp_number}
      </h2>
      <VideoFeedSection className="some-space">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
        />
        <div className="captured-img">
          {numImages.map((item, i) => (
            <DataVideoSet
              parData1={parData}
              videoRef={webcamRef}
              key1={i}
              key={i}
              item={item}
              updateImageData={updateImageData}
            />
          ))}
        </div>

        {/* <button onClick={capture}>Capture photo</button> */}
        <button onClick={saveImage} className="testing">
          Save Image
        </button>
      </VideoFeedSection>
    </>
  );
};

export default VideoFeed;
