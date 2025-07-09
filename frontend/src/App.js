import { BrowserRouter, Routes, Route } from "react-router-dom";
import SplashScreen from "../src/components/SplashScreen";
import Home from "../src/components/Home";
import Admin from "./components/Admin";
import ViewStud from "./components/ViewStud";
import AddStud from "./components/AddStud";
import UpdateStud from "./components/UpdateStud";

function App() {
  return (
    <BrowserRouter>
    <Routes>

      <Route path="/" element={<SplashScreen/>}/>
       <Route path="/home" element={<Home />} />
      <Route path="/admin" element={<Admin />}>
      <Route index element={<ViewStud />} />
      <Route path="view" element={<ViewStud />} />
       <Route path="add" element={<AddStud />} />
       <Route path="update" element={<UpdateStud />} />
      </Route>
    </Routes>
    </BrowserRouter>
  );
}

export default App;