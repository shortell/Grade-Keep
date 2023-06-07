// import { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

const defaultTheme = createTheme({
    palette: {
        primary: {
            main: '#007d62',
        },
        secondary: {
            main: '#005a7d',
        },
    },
});

// TODO remove, this demo shouldn't need to reset the theme.

export default function SignUp() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const account_type = data.get('row-radio-buttons-group')
        const first_name = data.get('first_name')
        const last_name = data.get('last_name')
        const username = data.get('username')
        const password = data.get('password')
        const json = JSON.stringify({
            account_type: account_type,
            username: username,
            password: password,
            first_name: first_name,
            last_name: last_name
        })
        console.log(json)
        fetch('http://127.0.0.1:5000/register', {
            method: "POST",
            headers: { "Content-Type": "application/json", },
            body: json
        }).then(function (response) {
            console.log("success " + response.status  );
        }).catch(function (response) {
            console.log("fail" + response);
        })
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign up
                    </Typography>
                    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    name="first_name"
                                    required
                                    fullWidth
                                    id="first_name"
                                    label="First Name"
                                    autoFocus
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    id="last_name"
                                    label="Last Name"
                                    name="last_name"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    id="username"
                                    label="Username"
                                    name="username"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    name="password"
                                    label="Password"
                                    type="password"
                                    id="password"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    name="c-password"
                                    label="Confirm Password"
                                    type="password"
                                    id="c-password"
                                />
                            </Grid>
                        </Grid>
                        <FormControl name="account_type">
                            <FormLabel id="radio-buttons-group"  >I am a:</FormLabel>
                            <RadioGroup
                                id="account_type"
                                row
                                name="row-radio-buttons-group"
                            >
                                <FormControlLabel id="teacher-radio" value="teacher" control={<Radio />} label="Teacher" />
                                <FormControlLabel id="student-radio" value="student" control={<Radio />} label="Student" />
                            </RadioGroup>
                        </FormControl>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign Up
                        </Button>
                        <Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link component={RouterLink} to="/signin" variant="body2" color='secondary'>
                                    {"Already have an account? Sign in"}
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}