import useStyles from "../../style";
import AllNotes from "../note/AllNotes";
import Sidebar from "./Sidebar";

export default function Main() {
  const classes = useStyles();
  return (
    <>
      <Sidebar />
      <main className={classes.main}>
      
        <AllNotes />
      
      </main>
    </>
  )
}