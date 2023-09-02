export default function Sidebar() {
  return (
    <aside className="sidebar">
      <ul className="sidebar__menu">
        <li className="sidebar__menu-item">
          <a href="/dashboard">Dashboard</a>
        </li>
        <li className="sidebar__menu-item">
          <a href="/dashboard/subjects">Subjects</a>
        </li>
        <li className="sidebar__menu-item">
          <a href="/dashboard/teachers">Teachers</a>
        </li>
        <li className="sidebar__menu-item">
          <a href="/dashboard/students">Students</a>
        </li>
        <li className="sidebar__menu-item">
          <a href="/dashboard/grades">Grades</a>
        </li>
      </ul>
    </aside>
  );
}
