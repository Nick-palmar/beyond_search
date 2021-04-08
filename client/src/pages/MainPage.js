import React, { useState, useEffect, useRef } from "react";
import { Typography, Grid, withStyles, Card, CardContent, Container, Snackbar, CardHeader, IconButton } from '@material-ui/core'
import InputTextField from '../components/InputTextField';
import LiveTextField from '../components/LiveTextField';
import SmallButton from '../components/SmallButton';
import { Add, Search, Delete } from '@material-ui/icons';
import { Alert } from '@material-ui/lab';
import ResultStrings from '../components/ResultStrings';
import axios from 'axios';

const FormData = require('form-data');

// const textFieldInfo = [
//     {
//         fieldName: 'Repo Name',
//         icon: <Add style={{color: '#7b113a'}}/>,
//         helperText: 'Add a repo'
//     },
//     {
//         fieldName: 'Repo Name',
//         icon: <Search style={{color: '#7b113a'}}/>,
//         helperText: 'Search for repo'
//     }
// ]

// const rows = [
//     {
//         id: 1,
//         repoName: 'Repo 1',
//         userName: 'Test 1'
//     },
//     {
//         id: 2,
//         repoName: 'Repo 2',
//         userName: 'Test 2'
//     },
//     {
//         id: 3,
//         repoName: 'Repo 3',
//         userName: 'Test 3'
//     }, 
//     {
//         id: 4,
//         repoName: 'Repo 1',
//         userName: 'Test 1'
//     },
//     {
//         id: 5,
//         repoName: 'Repo 2',
//         userName: 'Test 2'
//     },
//     {
//         id: 6,
//         repoName: 'Repo 3',
//         userName: 'Test 3'
//     }
// ];


const MainPage = () => {

    // initialize constants
    const base_api_url = 'https://beyond-search.herokuapp.com/api';
    const isInitMount = useRef(true);
    // set the states of the fields
    const [fieldObj, setFieldObj] = useState({addUser: '', searchRepo: ''})
    const [flash, setFlash] = useState({'open': false, 'status': null});
    const [rows, setRows] = useState([])
    const [emptySearch, setEmptySearch] = useState(true);


    // create a trie when the page loads
    useEffect(() => {
        // console.log(emptySearch);
        if (isInitMount.current) {
            // handle on mount
            const fetchTrie = async() => {
                const create_trie_endpoint = base_api_url + '/create-trie';
                const res = await axios.get(create_trie_endpoint);
                const data = res.data;
                console.log(data);
            };
            fetchTrie();
            isInitMount.current = false;
            console.log('Initial Mount');
        }
        else {
            // axios cancellation variables
            const CancelToken = axios.CancelToken;
            const source = CancelToken.source();

            // handle component on update to search trie
            const search_trie_endpoint = base_api_url + '/search-trie';
            const fetchSearchTrie = async() => {
                try {
                    const res = await axios.get(search_trie_endpoint, { 
                        params: { 'searchString': fieldObj['searchRepo'],
                        cancelToken: source.token,
                        // timeout: 0.0000000000000001
                    }});
                    // check to see if the textbox is empty - clear
                    console.log(emptySearch);
                    if (emptySearch && fieldObj['searchRepo'] !== '') {
                        console.log('Cancelled request')
                        source.cancel();
                        setRows([]);
                        return;
                    }
                    // request is most up to data - update rows
                    console.log(fieldObj['searchRepo']);
                    const data = res.data;
                    setRows(data);
                    console.log(data);
                }
                catch (err) {
                    console.log(err);
                }
            }
            fetchSearchTrie();
            console.log('Fetch Search: ' +  fieldObj['searchRepo']) 
        }
  
    }, [ fieldObj['searchRepo'] ]);

    const BurgendyTextTypography = withStyles({
        root: {
          color: "#150e56"
        }
      })(Typography);

    const flashMessage = (status) => {
        if (status === 'success') {
            setFlash({ 'open': true, 'status': 'success'});
        }
        else {
            setFlash({ 'open': true, 'status': 'error'});
        }
      };
    
      const handleClose = (event) => {
        setFlash(prevState => {
            return { ...prevState, 'open': false};
        });
      };

    // const setLastSearch = (value) => {
    //     _lastSearch = value;
    //     console.log(_lastSearch)
    // }
    // const getLastSearch = () => {
    //     console.log('Getter' + _lastSearch)
    //     return _lastSearch;
    // }

    const changeRepo = async(e, field) => {
        // console.log(fieldObj)
        // change the value of add repo
        setFieldObj(prevState => {
            const currObj = {...prevState};
            currObj[field] = e.target.value;
            return currObj;
        });
        if (e.target.value === '') {
            setEmptySearch(true);
            console.log('cr' + true);
        }
        else {
            setEmptySearch(false);
            console.log('cr' + false);
        }

        // send a request to the backend if search repo is being touched
        // if (field === 'searchRepo') {
        //     const search_trie_endpoint = base_api_url + '/search-trie';
        //     try {
        //         const res = await axios.get(search_trie_endpoint, { params: { 'searchString': e.target.value }});
        //         const data = res.data;
        //         setRows(prevState => {
        //             // const newRows = { ...data };
        //             return data;
        //         });
        //         console.log(data);
        //     }
        //     catch (err) {
        //         console.log(err);
        //     }
        // }
    }

    const addUser = async(e) => {
        // send post request to backend
        const add_user_endpoint = base_api_url + '/add-user';
        const form_data = new FormData();
        form_data.append('userName', fieldObj['addUser']);
        // console.log(add_user_endpoint);
        // console.log(user);
        try {
            const res = await axios.post(add_user_endpoint, form_data);
            const data = res.data;
            console.log(data);
            flashMessage('success');
        }
        catch (err) {
           flashMessage('error');
        }

        // clear the user from the object
        setFieldObj(prevState => {
            const currObj = {...prevState};
            currObj['addUser'] = '';
            return currObj;
        })

        // depending on the data, flash a message to the user

    }

    const handleDeleteClicked = async() => {
        // delete all users from trie 
        const delete_users_endpoint = base_api_url + '/truncate/8';
        const res = await axios.delete(delete_users_endpoint);
        console.log('Data Deleted');
    }

    return (
        <>
        <Container maxWidth='xs'>
            <Grid container spacing={8} alignItems='center' justify="center" style={{ minHeight: '100vh' }}>
                <Grid item xs={12} className='title' align='center'>
                    <BurgendyTextTypography variant='h2'> Beyond Search </BurgendyTextTypography>
                </Grid>
                
                <Grid item xs={12} align='center'>
                    <Card>
                        <CardHeader
                            action={
                                    <IconButton aria-label="delete" onClick={handleDeleteClicked}>
                                        <Delete style={{color: '#880e4f'}} />
                                    </IconButton>
                            }
                        />
                        <CardContent>
                            <InputTextField fieldValue={fieldObj['addUser']} fieldName='User Name' icon={ <Add style={{color: '#7b113a'}} /> } helperText= 'Add a github user' updateTextField={changeRepo}/>
                            <SmallButton buttonClicked={addUser}/>
                        </CardContent>
                    </Card>
                </Grid>

                <Snackbar anchorOrigin={{ vertical: 'center', horizontal: 'center' }} open={flash['open']} autoHideDuration={3000} onClose={handleClose}>
                    <Alert onClose={handleClose} severity={flash['status']}>
                        {(flash['status'] === 'success') ? 'User Added!': 'User Not Added :('}
                    </Alert>
                </Snackbar>

                <Grid item xs={12} align='center'>
                    <Card>
                            <CardContent>
                                <InputTextField fieldValue={fieldObj['searchRepo']} fieldName='Repo Name' icon={ <Search style={{color: '#7b113a'}} /> } helperText= 'Search for repo' updateTextField={changeRepo}/>
                            </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} align='center'>
                    <ResultStrings rows={rows}/>
                </Grid>
              
            </Grid>
            </Container>
        </>
    );
};

export default MainPage;