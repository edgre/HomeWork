import React, { useState } from "react";
import "../../assets/styles/dropDown.css";
import "../../assets/styles/authPage.css";

const DropdownList = () => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");

  const categories = [
    {
      id: "researchWorks",
      name: "ВУЗ научные работы",
      subcategories: [
        { id: "coursework", name: "Курсовая работа" },
        { id: "research", name: "Научно-исследовательская работа" },
        { id: "diploma", name: "Диплом" },
        { id: "vkr", name: "ВКР" },
      ],
    },
    {
      id: "laboratoryWorks",
      name: "ВУЗ лабораторные работы",
      subcategories: [
        { id: "lab-programming", name: "Программирование" },
        { id: "lab-secmodel", name: "Модели безопасности" },
        { id: "lab-networks", name: "Компьютерные сети" },
        { id: "lab-tchmk", name: "ТЧМК" },
        { id: "lab-plangs", name: "Языки программирования" },
      ],
    },
    {
      id: "universityTasks",
      name: "ВУЗ задачи",
      subcategories: [
        { id: "high-mathanalisis", name: "Мат. анализ" },
        { id: "high-economics", name: "Экономика" },
        { id: "high-kmzi", name: "КМЗИ" },
        { id: "high-cryptography", name: "Криптография" },
        { id: "high-statistics", name: "Мат. статистика" },
        { id: "high-probability", name: "Теория вероятности" },
        { id: "high-algebra", name: "Алгебра" },
        { id: "high-programming", name: "Программирование" },
      ],
    },
    {
      id: "schoolTasks",
      name: "Школа задачи",
      subcategories: [
        { id: "school-algebra", name: "Алгебра" },
        { id: "school-geometry", name: "Геометрия" },
        { id: "school-physics", name: "Физика" },
        { id: "school-informatics", name: "Информатика" },
      ],
    },
  ];

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
    setSelectedSubcategory("");
  };

  const handleSubcategoryChange = (e) => {
    setSelectedSubcategory(e.target.value);
  };

  const currentSubcategories = selectedCategory
    ? categories.find((c) => c.id === selectedCategory).subcategories
    : [];

  return (
    <>
      <div className="form-group">
        {/* <label className="dropdown-label">Категория</label> */}
        <select
          className="dropdown-select"
          value={selectedCategory}
          onChange={handleCategoryChange}
        >
          <option value="">Выберите категорию</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <select
          className="dropdown-select"
          value={selectedSubcategory}
          onChange={handleSubcategoryChange}
          disabled={!selectedCategory}
        >
          <option value="">
            {selectedCategory
              ? "Выберите предмет"
              : "Сначала выберите категорию"}
          </option>
          {currentSubcategories.map((subcategory) => (
            <option key={subcategory.id} value={subcategory.id}>
              {subcategory.name}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

export default DropdownList;
