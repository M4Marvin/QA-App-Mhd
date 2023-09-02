import Dashboard from "./ProfessorList";
import WithRole from "./WithRole";

const roles = ["Headmaster", "QA Officer"];
const DashboardWithRole = WithRole(Dashboard, roles);

export default function ProtectedDashboard() {
  return <DashboardWithRole />;
}
