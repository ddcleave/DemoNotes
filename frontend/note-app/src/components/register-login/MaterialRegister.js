import React from 'react';
import * as yup from 'yup';
import { useHistory } from 'react-router-dom'
import useStyles from '../../style';
import { useFormik } from 'formik';
import { Dialog, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import signupAPI from '../utils/API/signup';

const validationSchema = yup.object({
    username: yup
      .string()
      .min(3, 'Username should be of minimum 3 characters length')
      .max(50, 'Username should be of maximum 50 characters length')
      .required('Required'),
    password: yup
      .string()
      .min(8, 'Password should be of minimum 8 characters length')
      .max(50, 'Password should be of maximum 50 characters length')
      .required('Password is required'),
    password_again: yup
      .string()
      .required('Re-enter password'),
    email: yup
      .string()
      .email('Enter a valid email')
      .required('Email is required'),
    fullname: yup
      .string()
      .required('Fullname is required')
      .min(3, 'Fullname should be of minimum 3 characters length')
      .max(50, 'Fullname should be of maximum 50 characters length')
});

export default function MaterialRegister(props) {
  const { open, handleClose } = props
  const classes = useStyles()
  
  let history = useHistory();
  const formik = useFormik({
    initialValues: {
      username: '',
      email: '',
      password: '',
      password_again: ''
    },
    validationSchema: validationSchema,
    validate: (values => {
      const errors = {};
      if (values.password !== values.password_again) {
          errors.password_again = 'Passwords don\'t match';
      } else if (
          !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
      ) {
          errors.email = 'Invalid email address';
      }
      return errors;
    }),
    onSubmit: (async (values) => {
      const response = await signupAPI(values)
      if (response.ok) {
        history.push("/");
      }
    })
  });

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle className={classes.loginTitle}>Registration</DialogTitle>
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
                id="email"
                name="email"
                label="Email"
                value={formik.values.email}
                onChange={formik.handleChange}
                error={formik.touched.email && Boolean(formik.errors.email)}
                helperText={formik.touched.email && formik.errors.email}
              />
              <TextField
                fullWidth
                id="fullname"
                name="fullname"
                label="Fullname"
                value={formik.values.fullname}
                onChange={formik.handleChange}
                error={formik.touched.fullname && Boolean(formik.errors.fullname)}
                helperText={formik.touched.fullname && formik.errors.fullname}
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
              <TextField
                fullWidth
                id="password_again"
                name="password_again"
                label="Password_again"
                type="password"
                value={formik.values.password_again}
                onChange={formik.handleChange}
                error={formik.touched.password_again && Boolean(formik.errors.password_again)}
                helperText={formik.touched.password_again && formik.errors.password_again}
              />
              <Button color="primary" variant="contained" fullWidth type="submit"
                className={classes.loginButton}
              >
                Sign up
              </Button>
            </form>
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </div>
  );
};