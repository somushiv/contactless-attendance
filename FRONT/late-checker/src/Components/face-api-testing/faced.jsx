import React, { useState, useEffect, useCallback } from "react";

import { loadModels, getFullFaceDescription } from "../../faceapi/FaceAPI";
const testImg = require("../../img/Cherprang.jpeg");
// Initial State
const INIT_STATE = {
  imageURL: testImg,
  fullDesc: null,
  detections: null,
};
const FacedTesting = () => {
  const [state, setState] = useState(INIT_STATE);
  //const [drawBox, setDrawBox] = useState(null);

  useEffect(() => {
    async function featchdata() {
      await loadModels();
      await handleImage(state.imageURL);
    }
    featchdata();
  }, []);
  const handleImage = async (imageRef = state.imageURL) => {
    await getFullFaceDescription(imageRef).then((fullDesc) => {
      const tmpState = { ...state };

      setState(tmpState);
      if (!!fullDesc) {
        tmpState["fullDesc"] = fullDesc;
        tmpState["detections"] = fullDesc.map((fd) => fd.detection);
        setState(tmpState);
        renderBox();
      }
    });
  };
  const test = () => {
    const tmpState = { ...state };
    tmpState["fullDesc"] = "testing";
    setState(tmpState);
  };
  //   const handleFileChange = async (event) => {
  //     resetState();
  //     await setState({
  //       imageURL: URL.createObjectURL(event.target.files[0]),
  //       loading: true,
  //     });
  //     handleImage();
  //   };

  const resetState = () => {
    setState({ ...INIT_STATE });
  };

  const renderBox = () => {
    const { imageURL, detections } = state;
    let drawBox = null;
    if (!!detections) {
      drawBox(
        detections.map((detection, i) => {
          let _H = detection.box.height;
          let _W = detection.box.width;
          let _X = detection.box._x;
          let _Y = detection.box._y;
          return (
            <div key={i}>
              <div
                style={{
                  position: "absolute",
                  border: "solid",
                  borderColor: "blue",
                  height: _H,
                  width: _W,
                  transform: `translate(${_X}px,${_Y}px)`,
                }}
              />
            </div>
          );
        })
      );
    }
  };
  return (
    <>
      <div>Testing Facial</div>
      {/* <input
        id="myFileUpload"
        type="file"
        onChange={handleFileChange}
        accept=".jpg, .jpeg, .png"
      /> */}

      <div style={{ position: "relative" }}>
        <div style={{ position: "absolute" }}>
          <img src={state.imageURL} alt="imageURL" />
          <button className="btn btn-primary" onClick={handleImage}>
            Render
          </button>
        </div>
        {/* {!!drawBox ? drawBox : null} */}
      </div>
    </>
  );
};

export default FacedTesting;
