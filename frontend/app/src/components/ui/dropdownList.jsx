import React, { useState } from "react";
import "../../assets/styles/dropDown.css";
import "../../assets/styles/authPage.css";

const DropdownList = ({ onCategoryChange, onSubcategoryChange }) => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");

  // Категории и подкатегории, где id и name совпадают
  const categories = [
    {
      id: "Научные работы",
      name: "Научные работы",
      subcategories: [
        { id: "Курсовая работа", name: "Курсовая работа" },
        { id: "Научно-исследовательская работа", name: "Научно-исследовательская работа" },
        { id: "Диплом", name: "Диплом" },
        { id: "ВКР", name: "ВКР" },
      ],
    },
    {
      id: "Лабораторные работы",
      name: "Лабораторные работы",
      subcategories: [
        { id: "Программирование", name: "Программирование" },
        { id: "Модели безопасности", name: "Модели безопасности" },
        { id: "Компьютерные сети", name: "Компьютерные сети" },
        { id: "ТЧМК", name: "ТЧМК" },
        { id: "Языки программирования", name: "Языки программирования" },
      ],
    },
    {
      id: "Университетские задачи",
      name: "ВУЗ задачи",
      subcategories: [
        { id: "Мат. анализ", name: "Мат. анализ" },
        { id: "Экономика", name: "Экономика" },
        { id: "КМЗИ", name: "КМЗИ" },
        { id: "Криптография", name: "Криптография" },
        { id: "Мат. статистика", name: "Мат. статистика" },
        { id: "Теория вероятности", name: "Теория вероятности" },
        { id: "Алгебра", name: "Алгебра" },
        { id: "Программирование", name: "Программирование" },
      ],
    },
    {
      id: "Школьные задачи",
      name: "Школа задачи",
      subcategories: [
        { id: "Алгебра", name: "Алгебра" },
        { id: "Геометрия", name: "Геометрия" },
        { id: "Физика", name: "Физика" },
        { id: "Информатика", name: "Информатика" },
      ],
    },
  ];

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setSelectedCategory(value);
    setSelectedSubcategory("");
    onCategoryChange(value);
  };

  const handleSubcategoryChange = (e) => {
    const value = e.target.value;
    setSelectedSubcategory(value);
    onSubcategoryChange(value);
  };

  const currentSubcategories = selectedCategory
    ? categories.find((c) => c.id === selectedCategory)?.subcategories || []
    : [];

  return (
    <>
      <div className="form-group">
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