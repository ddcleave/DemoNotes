import { Button } from "@material-ui/core";
import { useState } from "react";


export default function ButtonForDialog(props) {
  const { Element, name } = props
  const [open, setOpen] = useState(false)

  const handleClick = () => {
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
  }

  return (
    <>
      <Button style={{ color: '#FFF' }} color="inhirit" onClick={handleClick}>
        {name}
      </Button>
      <Element open={open} handleClose={handleClose} />
    </>
  )
}