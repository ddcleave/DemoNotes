import React, { useState, useEffect } from "react"
import useStyles from "../../style";
import { useSelector, useDispatch } from 'react-redux'
import { Route} from "react-router-dom"
import Hello from "../Hello";
import MaterialLogin from "../register-login/MaterialLogin";
import MaterialRegister from "../register-login/MaterialRegister";
import { AppBar, CircularProgress, Toolbar, Typography, Button } from "@material-ui/core";
import { setUnauthorized, successAuth } from "./authSlice";
import CssBaseline from '@material-ui/core/CssBaseline';
import VerifyEmail from "./verify";
import Main from "./Main";
import ButtonForDialog from "../register-login/ButtonForDialog";
import logoutAPI from "../utils/API/logout";
import checkAPI from "../utils/API/check";
import { resetData } from "../note/notesSlice";


export default function Dashboard() {
  const classes = useStyles()
  const auth = useSelector((state) => state.auth)
  const dispatch = useDispatch()


  const handleLogout = async () => {
    const response = await logoutAPI()
    if (response.ok) {
      dispatch(resetData())
    }
  }

  useEffect(() => {
    async function getUsername() {
      const response = await checkAPI()
      
      if (response.ok) {
        const data = await response.json()
        dispatch(successAuth(data.username))
      }
      else {
        dispatch(setUnauthorized())
      }
    }
    if (auth.status === 'idle') {
      getUsername()
    }
  }, [auth])

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar 
        style={{zIndex: 1201}}
      // className={classes.AppBar} 
        position='fixed'
      >
        <Toolbar>
          <Typography variant="h6" className={classes.appBarTitle}>
            DemoNotes
          </Typography>
          { auth.status === "false" && (
            <>
              <ButtonForDialog name="Sign Up" Element={MaterialRegister} />
              <ButtonForDialog name="Sign In" Element={MaterialLogin} />
            </>
          )}
          
          { auth.status === "true" && (
            <Button style={{ color: '#FFF' }} onClick={handleLogout}>Log out</Button>
          )}
        </Toolbar>
      </AppBar>
      <div className={classes.sidebarAndMain}>
      <Route path='/' exact >
        { auth.status === "false" && <Hello />}
      </Route>

        { auth.status === "idle" && <CircularProgress className={classes.progress} />}
        { auth.status === "true" && <Main />}

      <Route path='/verify' component={VerifyEmail} />
      </div>
    </div>
  )
}