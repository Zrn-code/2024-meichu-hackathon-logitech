import "./styles.css";
import * as THREE from "three";
import { Canvas, useThree } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import { OrbitControls, Environment } from "@react-three/drei";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { MTLLoader } from "three/examples/jsm/loaders/MTLLoader";
import { DDSLoader } from "three-stdlib";
import rawData from "./generated_data.json";

THREE.DefaultLoadingManager.addHandler(/\.dds$/i, new DDSLoader());

// 過濾掉 model_id 為 None 的項目
const filteredData = rawData.filter((item) => item.model_id);

const Scene = ({ modelId }) => {
  const groupRef = useRef();
  const { scene } = useThree();

  useEffect(() => {
    if (!modelId) return; // 確保 modelId 存在

    // Load MTL file
    const mtlLoader = new MTLLoader();
    mtlLoader.load(`models/${modelId}/${modelId}.mtl`, (materials) => {
      materials.preload();

      // Load OBJ file once materials are ready
      const objLoader = new OBJLoader();
      objLoader.setMaterials(materials);
      objLoader.load(`models/${modelId}/${modelId}.obj`, (object) => {
        if (groupRef.current) {
          groupRef.current.clear(); // Clear previous model
          groupRef.current.add(object);
          const scaleFactor = 2; // 調整此值以改變大小
          object.scale.set(scaleFactor, scaleFactor, scaleFactor);
        }
      });
    });
  }, [scene, modelId]);

  return <group ref={groupRef} />;
};

const Card = ({ id, type, onClick }) => {
  let imageSrc = "";
  let title = "";

  switch (type) {
    case "Sketch":
      imageSrc = `sketch/${id}.png`;
      title = "Sketch";
      break;
    case "Background":
      imageSrc = `background/${id}.png`;
      title = "Background";
      break;
    case "Result":
      imageSrc = `result/${id}.png`;
      title = "Result";
      break;
    default:
      title = "Unknown";
      break;
  }

  return (
    <div
      className="max-w-full rounded overflow-hidden shadow-lg"
      onClick={onClick}
    >
      <img className="w-full" src={imageSrc} alt={title} />
      {/* 你可以選擇添加標題 */}
      {/* <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{title}</div>
      </div> */}
    </div>
  );
};

export default function App() {
  const [modelIndex, setModelIndex] = useState(0);
  const [type, setType] = useState("Sketch");
  const [preview, setPreview] = useState("Preview");
  const typeOrder = ["Sketch", "Background", "Result", "Model"];
  const currentModelId = filteredData[modelIndex].model_id;
  const currentSketchId = filteredData[modelIndex].sketch_id;

  // 點擊圖片的處理函數
  const handleSketchClick = (id) => {
    // 更新 preview 狀態並設置當前 sketch ID
    setPreview("NotPreview");
    setModelIndex(filteredData.findIndex((item) => item.sketch_id === id));
  };
  const handleNextType = () => {
    setType((prevType) => {
      const currentIndex = typeOrder.indexOf(prevType);
      return typeOrder[(currentIndex + 1) % typeOrder.length];
    });
  };

  const handlePreviousType = () => {
    setType((prevType) => {
      const currentIndex = typeOrder.indexOf(prevType);
      return typeOrder[
        (currentIndex - 1 + typeOrder.length) % typeOrder.length
      ];
    });
  };

  return (
    <div className="flex flex-col justify-center items-center h-screen w-screen app-background">
      <div
        className={`relative w-5/6 ${
          type === "Model" ? "h-3/5" : "h-auto"
        } border-4 rounded border-black m-5`}
      >
        {preview === "Preview" ? (
          filteredData.map(
            (item) =>
              item.sketch_id && (
                <Card
                  key={item.sketch_id}
                  id={item.sketch_id}
                  type="Sketch"
                  onClick={() => handleSketchClick(item.sketch_id)} // 點擊處理函數
                />
              )
          )
        ) : (
          <Card id={currentSketchId} type="Sketch" />
        )}

        {/* 這裡可以添加其他需要顯示的內容 */}
      </div>

      <div className="flex space-x-4 mt-5">
        {/* 當 type 是 Sketch 時，不顯示 Prev Type 按鈕 */}
        {type !== "Sketch" && (
          <button
            className="p-2 bg-blue-500 text-white rounded"
            onClick={handlePreviousType}
          >
            上一個型別
          </button>
        )}

        {/* 當 type 是 Model 時，不顯示 Next Type 按鈕 */}
        {type !== "Model" && (
          <button
            className="p-2 bg-blue-500 text-white rounded"
            onClick={handleNextType}
          >
            下一個型別
          </button>
        )}
      </div>
    </div>
  );
}



import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Preview from './Preview';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:id" element={<Preview />} />
      </Routes>
    </Router>
  );
}

function Home() {
  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-4xl font-bold">Welcome to My Project</h1>
    </div>
  );
}

export default App;
