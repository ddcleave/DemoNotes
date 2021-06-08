import React, { useState, useEffect } from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { useHistory } from 'react-router-dom'
import { Dialog, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import useStyles from '../../style';
import { useDispatch } from 'react-redux'
import { successAuth } from '../control/authSlice';
import { fpPromise } from '../..';
import signinAPI from '../utils/API/signin';


const validationSchema = yup.object({
  username: yup
    .string()
    .min(3, 'Username should be of minimum 3 characters length')
    .max(50, 'Username should be of maximum 50 characters length')
    .required('Username is required'),
  password: yup
    .string('Enter your password')
    .min(8, 'Password should be of minimum 8 characters length')
    .max(50, 'Password should be of maximum 50 characters length')
    .required('Password is required'),
});

export default function MaterialLogin(props) {
  const { open, handleClose } = props
  const classes = useStyles()
  const [fingerprint, setFingerprint] = useState();
  const dispatch = useDispatch()
  const getFingerprint = (async () => {
    const fp = await fpPromise
    const result = await fp.get();
    const visitorId = result.visitorId;
    setFingerprint(visitorId)
  });
  useEffect(() => {
    getFingerprint();
  }, [])
  const history = useHistory();
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema: validationSchema,
    onSubmit: (async (values) => {
      const response = await signinAPI(
        values.username,
        values.password,
        fingerprint
      )
      if (response.ok) {
        history.push("/");
        dispatch(successAuth(""))
      }
    })
  })

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle className={classes.loginTitle}>Sign in</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <form onSubmit={formik.handleSubmit}>
              <TextField
                fullWidth
                id="username"
                name="username"
                label="Username"
                value={formik.values.username}
                onChange={formik.handleChange}
                error={formik.touched.username && Boolean(formik.errors.username)}
                helperText={formik.touched.username && formik.errors.username}
              />
              <TextField
                fullWidth
                id="password"
                name="password"
                label="Password"
                type="password"
                value={formik.values.password}
                onChange={formik.handleChange}
                error={formik.touched.password && Boolean(formik.errors.password)}
                helperText={formik.touched.password && formik.errors.password}
              />
              <Button color="primary" variant="contained" fullWidth type="submit"
                className={classes.loginButton}
              >
                Sign in
              </Button>
            </form>
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </div>
  );
};
