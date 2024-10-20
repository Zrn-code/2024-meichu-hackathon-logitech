import React from "react";
import { useParams } from "react-router-dom";

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
    </div>
  );
};

export default function Preview() {
  const { id } = useParams();

  // 使用 findIndex 查找對應的索引
  const modelIndex = filteredData.findIndex((item) => item.sketch_id === id);

  const [type, setType] = useState("Sketch");
  const [environmentPreset, setEnvironmentPreset] = useState("sunset");

  const typeOrder = ["Sketch", "Background", "Result", "Model"];
  const currentModelId = filteredData[modelIndex]?.model_id;
  const currentSketchId = filteredData[modelIndex]?.sketch_id;
  const currentResultId = filteredData[modelIndex]?.result_id;
  const currentBackgroundId = filteredData[modelIndex]?.background_id;

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
  const getTitle = () => {
    switch (type) {
      case "Model":
        return "Result Model";
      case "Sketch":
        return "Sketch";
      case "Background":
        return "Background";
      case "Result":
        return "Result Image";
      default:
        return "";
    }
  };
  const handleChangeEnvironment = () => {
    const presets = ["sunset", "forest", "city", "dawn", "night", "warehouse"];
    const currentIndex = presets.indexOf(environmentPreset);
    const nextPreset = presets[(currentIndex + 1) % presets.length];
    setEnvironmentPreset(nextPreset);
  };
  return (
    <div className="flex flex-col justify-center items-center h-screen w-screen app-background">
      <h2 className="text-2xl font-bold mb-4 text-white">{getTitle()}</h2>
      <div
        className={`relative w-5/6 ${
          type === "Model" ? "h-3/5" : "h-auto"
        } border-4 rounded border-black m-5`}
      >
        {type === "Model" ? (
          <div className="w-full h-full">
            <Canvas style={{ width: "100%", height: "100%" }}>
              <Scene modelId={currentModelId} />
              <OrbitControls />
              <ambientLight intensity={0.8} />
              <directionalLight intensity={1.4} position={[2, 2, 2]} />
              <Environment preset={environmentPreset} background />
            </Canvas>
          </div>
        ) : (
          <Card
            id={
              type === "Sketch"
                ? currentSketchId
                : type === "Background"
                ? currentBackgroundId
                : currentResultId
            }
            type={type}
          />
        )}
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
        {type === "Model" && (
          <button
            className="p-2 bg-green-500 text-white rounded "
            onClick={handleChangeEnvironment}
          >
            Change Environment ({environmentPreset})
          </button>
        )}
      </div>
    </div>
  );
}
