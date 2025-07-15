// Icons component - centralized icon definitions
import { ImAccessibility, ImContrast } from "react-icons/im";
import { IoAccessibilitySharp } from "react-icons/io5";
import { VscRobot } from "react-icons/vsc";
import { CiLight } from "react-icons/ci";
import { CgDarkMode } from "react-icons/cg";


const Icons = {
  Send: () => <span>→</span>,
  Close: () => <span>×</span>,
  Info: () => <span>ℹ</span>,
  Help: () => <span>?</span>,
  Summary: () => <span>📋</span>,
  Refresh: () => <span>🔄</span>,
  Bot: () => <VscRobot/>,
  Settings: () => <span>⚙️</span>,
  Theme: () => <IoAccessibilitySharp />,
  Sun: () => <CiLight />,
  Moon: () => <CgDarkMode />,
  FontSize: () => <span>🔤</span>,
  Plus: () => <span>A+</span>,
  Minus: () => <span>A-</span>
};

export default Icons;
