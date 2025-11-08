// Icons component - centralized icon definitions
import { ImAccessibility, ImContrast } from "react-icons/im";
import { IoAccessibilitySharp } from "react-icons/io5";
import { VscRobot } from "react-icons/vsc";
import { CiLight } from "react-icons/ci";
import { CgDarkMode } from "react-icons/cg";
import { AiOutlineClose } from "react-icons/ai";


const Icons = {
  Send: () => <span>→</span>,
  Close: () => <AiOutlineClose />,
  Info: () => <span>ℹ</span>,
  Help: () => <span>?</span>,
  Summary: () => <span>📋</span>,
  Refresh: () => <span>🔄</span>,
  // Allow callers to pass props (size, className, color) so the icon can be styled consistently
  Bot: (props) => <VscRobot {...props} />,
  Settings: () => <span>⚙️</span>,
  Theme: () => <IoAccessibilitySharp />,
  Sun: () => <CiLight />,
  Moon: () => <CgDarkMode />,
  FontSize: () => <span>🔤</span>,
  Plus: () => <span>A+</span>,
  Minus: () => <span>A-</span>
};

export default Icons;
