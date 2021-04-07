import React from "react";
import { Typography, Grid } from '@material-ui/core'

const MainPage = () => {

    return (
        <>
            <Grid container spacing={0} className='page-container'>
                <Grid item xs={12} align='center' className='title'>
                    <Typography variant='h2'> Beyond Search </Typography>
                </Grid>
            </Grid>
        </>
    );
};

export default MainPage;