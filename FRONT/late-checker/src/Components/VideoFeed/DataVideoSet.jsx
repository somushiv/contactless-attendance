import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import "./videoStyle.css";

const DataVideoSet = ({ parData1, videoRef, key1, item, updateImageData }) => {
  const [imgPlaceHolder, setimgPlaceHolder] = useState("");
  const [imgData, setImgData] = useState("");
  const imageRef = useRef(null);

  const capture = React.useCallback(() => {
    const imageSrc = videoRef.current.getScreenshot();
    updateImageData(key1, imageSrc);
    setImgData(imageSrc);
    setimgPlaceHolder(<img src={imageSrc} id={item} ref={imageRef} />);
  }, [videoRef]);
  return (
    <>
      <div className="ref-img">
        {imgPlaceHolder}
        <button onClick={capture}>
          Capture photo {key1} {item}
        </button>
      </div>
    </>
  );
};

export default DataVideoSet;
