'use strict'

const webpack = require('webpack')
const { VueLoaderPlugin } = require('vue-loader')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')

const path = require('path')

// the path(s) that should be cleaned
let pathsToClean = [
  '../flask_app/vistor_app/templates'
]

// the clean options to use
let cleanOptions = {
    watch: true,
    verbose:  true,
    dry: false,
    allowExternal: true
}


module.exports = {
    mode: 'development',
    entry: [
        './src/main.js'
    ],
    devServer: {
        hot: true,
        watchOptions: {
            poll: true
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.ttf$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        outputPath: 'fonts/',
                        name: '[name].[ext]'
                    }
                }]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(pathsToClean, cleanOptions),
        new webpack.HotModuleReplacementPlugin(),
        new VueLoaderPlugin(),
        new CopyWebpackPlugin([
            {
                from: path.join(__dirname, 'src', 'assets', 'static'),
                to: path.join(__dirname, '..', 'flask_app', 'visitor_app','templates', 'static'),
                toType: 'dir',
                ignore: ['.gitkeep']
            }
        ]),
        new HtmlWebpackPlugin({
            filename: '../index.html',
            template: 'index.ejs',
            inject: true,
            title: "Visitor Signin"
        })
    ],
    output: {
        filename: 'bundle.js',
        path: path.join(__dirname, '..', 'flask_app', 'visitor_app','templates', 'static'),
    },
    target: 'web'
}
