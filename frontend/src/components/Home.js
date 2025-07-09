import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Home.css';
import { FaUserShield, FaGift, FaBirthdayCake } from 'react-icons/fa';
import { GiPartyPopper } from 'react-icons/gi';
import { Link } from 'react-router-dom';
import Confetti from 'react-confetti';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import Logo from "../assets/Logo.jpeg";
import confetti from 'canvas-confetti';


function Home() {
  const [birthdayBabies, setBirthdayBabies] = useState([]);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/get/')
      .then((res) => {setBirthdayBabies(res.data);console.log(res.data)})
      .catch(err => console.error(err));
  }, []);

   const sendBirthday = async () => {
    setShowConfirm(false); // Close modal

    if (birthdayBabies.length === 0) {
      alert("No students to send wishes.");
      return;
    }

    try {
      const res = await axios.post('http://localhost:5000/api/students/birthday', {
        students: birthdayBabies,
      });

      if (res.status === 200) {
        alert("Birthday wishes sent successfully!");
        confetti({
             angle: 90,
             spread: 360,
             startVelocity: 60,
             particleCount: 800,
             origin: { x: 0.5, y: 0.5 }
       
           });
      } else {
        alert("Failed to send birthday wishes.");
      }
    } catch (err) {
      console.error("Error sending birthday wishes:", err);
      alert("An error occurred while sending birthday wishes.");
    }
  };

  const handleWish = () => {

              setShowConfetti(true);
              setTimeout(()=>{
                setShowConfetti(false);
              },10000)
            }

  const responsive = {
    desktop: { breakpoint: { max: 3000, min: 1024 }, items: 3 },
    tablet: { breakpoint: { max: 1024, min: 600 }, items: 2 },
    mobile: { breakpoint: { max: 600, min: 0 }, items: 1 }
  };

  return (
    <div className="home-style">
      <nav className="navbar">
        <div className="logo-container">
          <Link to="/home" className="logo-link">
            <img src={Logo} alt="Logo" className="logo" />
            <span className="site-title">TEQ Wish</span>
          </Link>
        </div>
        <div className="nav-links">
          <Link to="/admin" className="logo-link">
            <button className="nav-button">
              <FaUserShield className="nav-icon" />
              <span className="nav-text">Admin</span>
            </button>
          </Link>
        </div>
      </nav>
      <div className='home-wish'>
        <h2 className="section-title">🎂 Today's Birthday Stars 🎉</h2>

      <div className="home-aravind">
        <Carousel
          responsive={responsive}
          infinite
          autoPlay
          autoPlaySpeed={2000}
          arrows={true}
          containerClass="carousel-container"
          itemClass="carousel-item"
          customTransition="transform 1000ms ease-in-out"
        >
          {birthdayBabies.map((student, index) => (
            <div className="home-birthday-card" key={index}>
              <div className="home-card-inner">
                <img src={student.image} alt={student.name} className="home-student-img" />
                <h3>Name: {student.name}</h3>
                <p>Reg.No: {student.regNo}</p>
                <FaGift className="home-gift-icon" />
              </div>
            </div>
          ))}
        </Carousel>
      </div>

      {showConfetti && <Confetti numberOfPieces={500} recycle={false} />}

      <button className="wish-button" onClick={() => setShowConfirm(true)}><FaBirthdayCake size={20} /></button>
      <button className="popper-button" onClick={handleWish} ><GiPartyPopper size={25} /></button>
      </div>

       {/* 🎂 Confirmation Popup */}
      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Send birthday wishes to students?</h3>
            <div className="modal-buttons">
              <button onClick={() => setShowConfirm(false)} className="cancel-btn">Cancel</button>
              <button onClick={sendBirthday} className="wish-btn">Wish</button>
            </div>
          </div>
        </div>
      )}
      
    </div>
  );
}

export default Home;
