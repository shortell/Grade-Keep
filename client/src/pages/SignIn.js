import * as React from 'react';
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

// TODO remove, this demo shouldn't need to reset the theme.


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

export default function SignIn() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const account_type = data.get('row-radio-buttons-group')
        const username = data.get('username')
        const password = data.get('password')
        const json = JSON.stringify({
            account_type: account_type,
            username: username,
            password: password,
        })
        console.log(json)
        fetch('http://127.0.0.1:5000/login', {
            method: "POST",
            headers: { "Content-Type": "application/json", },
            body: json
        }).then(function (response) {
            console.log("success " + response.status);
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
                        Sign in
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoFocus
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                        />
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
                            Sign In
                        </Button>
                        <Grid container>
                            <Grid item xs>
                            </Grid>
                            <Grid item>

                                <Link component={RouterLink} to="/signup" variant="body2" color='secondary'>
                                    {"Don't have an account? Sign Up"}
                                </Link>

                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}