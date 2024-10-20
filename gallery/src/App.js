import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import Preview from "./Preview";
import rawData from "./generated_data.json";

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
      className="rounded overflow-hidden shadow-lg cursor-pointer"
      onClick={onClick}
    >
      <img
        className="w-full h-auto object-contain"
        src={imageSrc}
        alt={title}
      />
    </div>
  );
};

function Home() {
  const navigate = useNavigate(); // 创建 navigate 实例
  const filteredData = rawData.filter((item) => item.model_id);

  const handleSketchClick = (id) => {
    navigate(`/${id}`); // 使用 navigate 跳转到对应 ID 的页面
  };

  return (
    <div className="flex flex-col items-center bg-black overflow-y-auto p-4">
      <div className="flex flex-wrap ">
        {filteredData.map(
          (item) =>
            item.sketch_id && (
              <div className="m-2">
                {" "}
                {/* Add margin to each card */}
                <Card
                  key={item.sketch_id}
                  id={item.sketch_id}
                  type="Sketch"
                  onClick={() => handleSketchClick(item.sketch_id)} // 點擊處理函數
                />
              </div>
            )
        )}
      </div>
    </div>
  );
}

export default App;
