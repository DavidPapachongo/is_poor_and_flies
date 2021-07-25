import React, { useState, useEffect,Component } from "react";
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import $ from 'jquery';

export default class SongList extends React.Component {
  constructor(props) {
    super(props);
    this.musClick = this.musClick.bind(this)
    this.state = {music: []};
  }

  componentDidMount() {
    this.SongList();
  }

  SongList() {
    $.getJSON('http://127.0.0.1:8000/songs/')
      .then(results  =>  {

        this.setState({ music: results })
      }
    );
  }

  musClick(Num, Like){
    this.setState({ Num: Num });
  }

  updateSong(id, song) {
    const newSongs = this.state.music.map(s => s.id === id ? song : s);
    this.setState({ music: newSongs })
  }

  render() {
    const songs = this.state.music.map((item, i) => (
      <div key={item.id}>
        <li value={item.id} onClick={() => this.musClick(item.id, item.liked)}>
          {item.song}
        </li>
        <LikeButton updateSong={(id, song) => this.updateSong(id, song)} Num={item.id} Like={item.liked} /> 
      </div>
    ));

    return (
      <div  id="layout-content" className="layout-content-wrapper">
        <div className="panel-list" >{ songs } </div>
        <AudioPlayer Num={this.state.Num} />,
      </div>
    );
  }
}


class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  } 
  
  handleClick() {
    const num = this.props.Num
    $.post(`http://127.0.0.1:8000/song/${num}/like`).then(song =>  {
        this.props.updateSong(song.id, song)
      }
    );

  }
  
  render() {
    const label = this.props.Like ? "unlike" : "like";
    return (
      <div className="customContainer">
        <button id="button" className="btn btn-primary" onClick={this.handleClick}>
          {label}</button>
      </div>
    );
  }
}



class AudioPlayer extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const num= this.props.Num
    const url = "http://127.0.0.1:8000/song/"+num+"/file"   
    
    return (
      <div>
        <audio id="my_Audio" controls onLoad>
          <source id="my_music" src={url} type="audio/mpeg"/>
        </audio>
      </div>
    );  
  }
  componentDidUpdate() {
    document.getElementById("my_Audio").load();
    document.getElementById("my_Audio").play();
  }
}

ReactDOM.render(
  <SongList/>,
  document.getElementById('root')
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
