import { useNavigate } from "react-router-dom";
import React, { useState, useRef, useEffect } from "react";
import "../assets/styles/grid.css";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom1 from "../components/ui/buttomHeader1";
import CapIcon from "../assets/images/GraduationCap.svg";
import ButtonWithIcon from "../components/ui/iconTextButton.jsx";

const categories = {
  laboratoryWorks: [
    { name: "Программирование", slug: "lab-programming" },
    { name: "Модели безопасности", slug: "lab-secmodel" },
    { name: "Компьютерные сети", slug: "lab-networks" },
    { name: "ТЧМК", slug: "lab-tchmk" },
    { name: "Языки программирования", slug: "lab-plangs" },
  ],
  researchWorks: [
    { name: "Курсовая работа", slug: "coursework" },
    { name: "Научно-исследовательская работа", slug: "research" },
    { name: "Диплом", slug: "diploma" },
    { name: "BKP", slug: "vkr" },
  ],
  schoolTasks: [
    { name: "Алгебра", slug: "school-algebra" },
    { name: "Геометрия", slug: "school-geometry" },
    { name: "Физика", slug: "school-physics" },
    { name: "Информатика", slug: "school-informatics" },
  ],
  universityTasks: [
    { name: "Мат. анализ", slug: "high-mathanalisis" },
    { name: "Экономика", slug: "high-economics" },
    { name: "КМЗИ", slug: "high-kmzi" },
    { name: "Криптография", slug: "high-cryptography" },
    { name: "Мат. статистика", slug: "high-statistics" },
    { name: "Теория вероятности", slug: "high-probability" },
    { name: "Алгебра", slug: "high-algebra" },
    { name: "Программирование", slug: "high-programming" },
  ],
};

const HomePage = () => {
  const navigate = useNavigate();
  // const [activeCategory, setActiveCategory] = useState(null);
  const labWorksRef = useRef(null);
  const researchRef = useRef(null);
  const schoolRef = useRef(null);
  const universityRef = useRef(null);

  const handleCardClick = (slug) => {
    navigate(`/category/${slug}`);
  };

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
        <HeaderTop username={"Gleb"} />
        <HeaderButtom1 />
      </header>

      <div className="grid">
        <div className="row-complete">
          <div className="row-header">Школьный курс • Задачи</div>
          <div className="row-cards" ref={schoolRef}>
            {categories.schoolTasks.map((task, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(task.slug)}
              >
                {task.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Задачи</div>
          <div className="row-cards" ref={universityRef}>
            {categories.universityTasks.map((task, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(task.slug)}
              >
                {task.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Лабораторные работы</div>
          <div className="row-cards" ref={labWorksRef}>
            {categories.laboratoryWorks.map((work, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(work.slug)}
              >
                {work.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Исследовательские работы</div>
          <div className="row-cards" ref={researchRef}>
            {categories.researchWorks.map((work, index) => (
              <ButtonWithIcon
                icon={CapIcon}
                key={index}
                className="card"
                onClick={() => handleCardClick(work.slug)}
              >
                {work.name}
              </ButtonWithIcon>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
