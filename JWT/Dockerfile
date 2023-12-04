# Use an official Node runtime as a parent image
FROM node:12-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY jwt-signature-apis-challenges .

# Install any needed packages specified in package.json
RUN npm install

# Make port 443 available to the world outside this container
EXPOSE 443

# Define environment variable
# You can define any environment variable that your app needs
ENV NODE_ENV=production

# Run app.js when the container launches
CMD ["node", "app.js"]