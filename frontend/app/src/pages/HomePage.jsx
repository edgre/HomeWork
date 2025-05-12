import { Link } from "react-router-dom";
import React, { useState, useRef, useEffect } from "react";
import "../assets/styles/grid.css";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom1 from "../components/ui/buttomHeader1";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import CapIcon from "../assets/images/GraduationCap.svg";
import ButtonWithIcon from "../components/ui/iconTextButton.jsx";

const categories = {
  laboratoryWorks: ["Программирование", "Химия", "Физика", "Механика", "Волны"],
  researchWorks: [
    "Курсовая работа",
    "Научно-исследовательская работа",
    "Диплом",
    "BKP",
  ],
  schoolTasks: [
    "Алгебра",
    "Геометрия",
    "Физика",
    "Литература",
    "Химия",
    "Обществознание",
    "География",
  ],
  universityTasks: [
    "Философия",
    "Экономика",
    "КМЗИ",
    "Криптография",
    "Мат. статистика",
    "ТРП",
    "Психология",
    "Теория вероятности",
    "Алгебра",
    "Программирование",
  ],
};

const HomePage = () => {
  const [activeCategory, setActiveCategory] = useState(null);
  const labWorksRef = useRef(null);
  const researchRef = useRef(null);
  const schoolRef = useRef(null);
  const universityRef = useRef(null);

  useEffect(() => {
    const setupHorizontalScroll = (ref) => {
      if (!ref.current) return;

      ref.current.addEventListener("wheel", (event) => {
        if (event.deltaMode === event.DOM_DELTA_PIXEL) {
          var modifier = 1;
        } else if (event.deltaMode === event.DOM_DELTA_LINE) {
          var modifier = parseInt(getComputedStyle(ref.current).lineHeight);
        } else if (event.deltaMode === event.DOM_DELTA_PAGE) {
          var modifier = ref.current.clientHeight;
        }

        if (event.deltaY !== 0) {
          ref.current.scrollLeft += modifier * event.deltaY;
          event.preventDefault();
        }
      });
    };

    setupHorizontalScroll(labWorksRef);
    setupHorizontalScroll(researchRef);
    setupHorizontalScroll(schoolRef);
    setupHorizontalScroll(universityRef);

    return () => {
      // Cleanup
      [labWorksRef, researchRef, schoolRef, universityRef].forEach((ref) => {
        if (ref.current) {
          ref.current.removeEventListener("wheel");
        }
      });
    };
  }, []);

  return (
    <div className="">
      <header>
        <HeaderTop />
        <HeaderButtom1 />
        {/* <HeaderButtom2 /> */}
      </header>

      <div className="grid">
        <div className="row-complete">
          <div className="row-header">ВУЗ • Лабораторные работы</div>
          <div className="row-cards" ref={labWorksRef}>
            {categories.laboratoryWorks.map((work, index) => (
              <button key={index} className="card">
                {work}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Исследовательские работы</div>
          <div className="row-cards" ref={researchRef}>
            {categories.researchWorks.map((work, index) => (
              <ButtonWithIcon icon={CapIcon} key={index} className="card">
                {work}
              </ButtonWithIcon>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">Школьный курс • Задачи</div>
          <div className="row-cards" ref={schoolRef}>
            {categories.schoolTasks.map((task, index) => (
              <button key={index} className="card">
                {task}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Задачи</div>
          <div className="row-cards" ref={universityRef}>
            {categories.universityTasks.map((task, index) => (
              <button key={index} className="card">
                {task}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
