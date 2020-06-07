import React, { useState, useRef } from "react";
import styled from "styled-components";
import "./videoStyle.css";
import Webcam from "react-webcam";
import DataVideoSet from "./DataVideoSet";

const videoConstraints = {
  facingMode: "user",
};

const VideoFeed = () => {
  const [parData, setParData] = useState("This is one its working");
  const numImages = ["somu1", "somu2", "somu3"];
  const VideoFeedSection = styled.section`
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    width: 45vw;
    h2 {
      font-size: 45px;
      line-height: 1;
      font-weight: normal;
      color: #013087;
      text-align: center;
    }
  `;

  const webcamRef = useRef(null);
  // const capture = React.useCallback(() => {
  //   const imageSrc = webcamRef.current.getScreenshot();
  //   console.log(imageSrc);
  //   setImgData(imageSrc);
  //   setimgPlaceHolder(<img src={imageSrc} id="profileImage" />);
  // }, [webcamRef]);

  // const saveImage = () => {
  //   fetch("http://127.0.0.1:5000/saveimage", {
  //     method: "POST",
  //     headers: {
  //       Accept: "application/json",
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify({ image_data: imgData }),
  //   })
  //     .then((reposonse) => reposonse.json())
  //     .then((response) => {
  //       console.log(response);
  //     });
  // };

  return (
    <>
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
              item={item}
            />
          ))}
        </div>

        {/* <button onClick={capture}>Capture photo</button> */}
        {/* <button onClick={saveImage}>Save Image</button> */}
      </VideoFeedSection>
    </>
  );
};

export default VideoFeed;
