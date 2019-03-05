#!/usr/bin/python3

from CS312Graph import *
import time
import math
# Note that |V| refers to the number of nodes/vertices in the network


# Class to keep track of each node and its index, distance, and previous node
# Time complexity is O(1) due to fast access of any arbitrary node
# Space complexity is O(|V|) because the dictionary is |V| length
class NodeDict(object):
    def __init__(self):
        self.node_dict = {}

    def __getitem__(self, key):
        return self.node_dict[key]

    def set_node(self, node, index, distance, previous):
        self.node_dict[node] = (index, distance, previous)


# Class implementation of priority queue unsorted array
# Time complexity is O(|V|) and space complexity is O(|V|)
class PriorityArray:
    def __init__(self, network, nodes):
        self.network = network
        self.queue = []
        self.node_dict = nodes
        self.make_queue()

    # Time and space complexity are both O(|V|)
    def make_queue(self):
        # Inserts each node into the unsorted list/array
        for node in self.network.nodes:
            self.insert(node)

    # Time complexity is O(1) and space complexity is O(|V|)
    def insert(self, node):
        # Appends specified node to the unsorted array
        self.queue.append(node)

    # Time complexity is O(|V|) and space complexity is O(1)
    def delete_min(self):
        # Initially set the current min to 0
        minimum = 0
        # Grab the distance of the first node in the array
        min_distance = self.node_dict[self.queue[0]][1]
        # Iterate through the unsorted array to find the smallest distance
        for i in range(len(self.queue)):
            # Grab the distance of the current node in the loop
            current_distance = self.node_dict[self.queue[i]][1]
            # Check to see if the selected distance is smaller than the current minimum
            if min_distance > current_distance:
                # Set the new minimum and keep track of its index
                min_distance = current_distance
                minimum = i
        # Return the final minimum node
        return self.queue.pop(minimum)

    # Don't need a decrease_key function for the array implementation
    # Time and space complexity are both O(1) since it just uses pass
    def decrease_key(self, node):
        pass


# Class implementation of priority queue minimum heap
# Time complexity is O(|V|log|V|) and space complexity is O(|V|)
class PriorityHeap:
    def __init__(self, network, nodes):
        self.network = network
        self.queue = []
        self.node_dict = nodes
        self.make_queue()

    # Time and space complexity are both O(|V|)
    def make_queue(self):
        # Inserts each node into the minimum heap
        for node in self.network.nodes:
            self.insert(node)

    # Time complexity is O(log|V|) and space complexity is O(|V|)
    def insert(self, node):
        # Set the current index to the length of the heap
        index = len(self.queue)
        # Append the selected node to the heap
        self.queue.append(node)
        # Grab the distance and previous node so we don't overwrite those values
        distance = self.node_dict[node][1]
        previous_node = self.node_dict[node][2]
        # Set the node in the dictionary
        self.node_dict.set_node(node, index, distance, previous_node)
        # Call the percolate up function for the current index
        self.percolate_up(index)

    # Time complexity is O(log|V|) and space complexity is O(1)
    def delete_min(self):
        # Grab the length of the current heap (minus 1)
        length = len(self.queue) - 1
        # Set the priority node to the first node in the heap
        priority_node = self.queue[0]
        # Set the last node to the last node in the heap
        last_node = self.queue[length]
        # Move the last node to the start of the heap
        self.queue[0] = last_node
        # Grab the priority's distance and previous node so we don't overwrite those values
        distance = self.node_dict[priority_node][1]
        previous_node = self.node_dict[priority_node][2]
        # Set the priority node in the dictionary
        self.node_dict.set_node(priority_node, 0, distance, previous_node)
        # Pop off the last node in the queue because it's a duplicate
        self.queue.pop(length)
        # Call the percolate down function on the first node in the heap
        self.percolate_down(0)
        # Return the priority node
        return priority_node

    # Time complexity is O(log|V|) and space complexity is O(1)
    def decrease_key(self, node):
        # Grab the index of the selected node and call percolate up on it
        index = self.node_dict[node][0]
        return self.percolate_up(index)

    # Time complexity is O(log|V|) and space complexity is O(1)
    def percolate_up(self, child_index):
        # Check to see if the specified index is the root and return if it is
        if child_index == 0:
            return
        # Otherwise grab the parent index using the child index
        parent_index = (child_index - 1) // 2
        # Grab the distances of the parent and child nodes
        parent_distance = self.node_dict[self.queue[parent_index]][1]
        child_distance = self.node_dict[self.queue[child_index]][1]

        # Check to see if we need to swap the parent and child nodes based on their distances
        if parent_distance > child_distance:
            # Swap the parent and child nodes in the heap
            self.queue[parent_index], self.queue[child_index] = self.queue[child_index], self.queue[parent_index]
            # Grab the new swapped nodes from the heap
            parent_node, child_node = self.queue[parent_index], self.queue[child_index]
            # Grab the parent's distance and previous node so we don't overwrite those values
            distance = self.node_dict[parent_node][1]
            previous_node = self.node_dict[parent_node][2]
            # Set the parent node in the dictionary
            self.node_dict.set_node(parent_node, parent_index, distance, previous_node)
            # Grab the child's distance and previous node so we don't overwrite those values
            distance = self.node_dict[child_node][1]
            previous_node = self.node_dict[child_node][2]
            # Set the child node in the dictionary
            self.node_dict.set_node(self.queue[child_index], child_index, distance, previous_node)
            # Call the percolate up function on the parent node's index
            return self.percolate_up(parent_index)

        # If we don't need to swap the nodes, just return
        else:
            return

    # Time complexity is O(log|V|) and space complexity is O(1)
    def percolate_down(self, parent_index):
        # Grab the length of the current heap
        length = len(self.queue)
        # Check to see if the parent index is the last node in the heap and return if it is
        if parent_index == length - 1:
            return
        # Otherwise grab the right and left indexes of the parent node's children
        right_index = (2 * parent_index) + 2
        left_index = (2 * parent_index) + 1
        # Check to see if the left child index is smaller than the heap's length
        # If it does, it has its own left child
        if left_index < length:
            # If the parent node's distance is greater than the left child node's distance
            if self.node_dict[self.queue[parent_index]][1] > self.node_dict[self.queue[left_index]][1]:
                # Check to see if the right child index is smaller than the heap's length
                # If it does, it has its own right child
                if right_index < length:
                    # If the right child node's distance is greater than or equal to the left child node's distance
                    if self.node_dict[self.queue[right_index]][1] >= self.node_dict[self.queue[left_index]][1]:
                        # Swap the parent and left child nodes in the heap
                        self.queue[parent_index], self.queue[left_index] = self.queue[left_index], self.queue[parent_index]
                        # Grab the new swapped nodes from the heap
                        parent_node, left_node = self.queue[parent_index], self.queue[left_index]
                        # Grab the parent's distance and previous node so we don't overwrite those values
                        distance = self.node_dict[parent_node][1]
                        previous_node = self.node_dict[parent_node][2]
                        # Set the parent node in the dictionary
                        self.node_dict.set_node(parent_node, parent_index, distance, previous_node)
                        # Grab the left child's distance and previous node so we don't overwrite those values
                        distance = self.node_dict[left_node][1]
                        previous_node = self.node_dict[left_node][2]
                        # Set the left child node in the dictionary
                        self.node_dict.set_node(self.queue[left_index], left_index, distance, previous_node)
                        # Call the percolate down function on the left child node's index and return its result
                        return self.percolate_down(left_index)
                    # Otherwise, the right child node is smaller
                    else:
                        # Swap the parent and right child nodes in the heap
                        self.queue[parent_index], self.queue[right_index] = self.queue[right_index], self.queue[parent_index]
                        # Grab the new swapped nodes from the heap
                        parent_node, right_node = self.queue[parent_index], self.queue[right_index]
                        # Grab the parent's distance and previous node so we don't overwrite those values
                        distance = self.node_dict[parent_node][1]
                        previous_node = self.node_dict[parent_node][2]
                        # Set the parent node in the dictionary
                        self.node_dict.set_node(parent_node, parent_index, distance, previous_node)
                        # Grab the right child's distance and previous node so we don't overwrite those values
                        distance = self.node_dict[right_node][1]
                        previous_node = self.node_dict[right_node][2]
                        # Set the right child node in the dictionary
                        self.node_dict.set_node(self.queue[right_index], right_index, distance, previous_node)
                        # Call the percolate down function on the right child node's index and return its result
                        return self.percolate_down(right_index)

        # Check to see if the right child index is smaller than the heap's length
        # If it does, it has its own right child
        if right_index < length:
            # If the parent node's distance is greater than the right child node's distance
            if self.node_dict[self.queue[parent_index]][1] > self.node_dict[self.queue[right_index]][1]:
                # Swap the parent and right child nodes in the heap
                self.queue[parent_index], self.queue[right_index] = self.queue[right_index], self.queue[parent_index]
                # Grab the new swapped nodes from the heap
                parent_node, right_node = self.queue[parent_index], self.queue[right_index]
                # Grab the parent's distance and previous node so we don't overwrite those values
                distance = self.node_dict[parent_node][1]
                previous_node = self.node_dict[parent_node][2]
                # Set the parent node in the dictionary
                self.node_dict.set_node(parent_node, parent_index, distance, previous_node)
                # Grab the right child's distance and previous node so we don't overwrite those values
                distance = self.node_dict[right_node][1]
                previous_node = self.node_dict[right_node][2]
                # Set the right child node in the dictionary
                self.node_dict.set_node(self.queue[right_index], right_index, distance, previous_node)
                # Call the percolate down function on the right child node's index and return its result
                return self.percolate_down(right_index)


# Class that finds and computes Dijkstra's shortest path
# Time and space complexity depend on if an unsorted array or heap is used
class NetworkRoutingSolver:
    def __init__(self):
        self.node_dict = NodeDict()

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network

    # Time and space complexity are both O(|V|)
    def getShortestPath(self, destIndex):
        self.dest = destIndex
        path_edges = []
        # Grab the destination node using the destIndex O(1)
        final_node = self.network.nodes[self.dest]
        # Set the current total length to the distance of the final node O(1)
        total_length = self.node_dict[final_node][1]
        # Set the current node to the final node for now
        current_node = final_node

        # Time complexity is O(|V|+|E|) which reduces to O(|V|)
        # V represents the nodes and E represents the edges
        # While the current node has a previous node (previous isn't nil) O(|V|)
        while self.node_dict[current_node][2] is not None:
            # Grab the previous node from the current node
            previous_node = self.node_dict[current_node][2]
            # Loop through each edge in the previous node's neighbors O(|E|)
            for edge in previous_node.neighbors:
                # Check to see if the edge's destination is our current node
                if edge.dest == current_node:
                    # If it is, append the edge to our array of path edges
                    path_edges.append((previous_node.loc, current_node.loc, '{:.0f}'.format(edge.length)))
            # Set the current node to the previous node
            current_node = previous_node
        # Return the total length as the cost and the array of edges for the path
        return {'cost': total_length, 'path': path_edges}

    # Time complexity is O(|V^2|) for an unsorted array
    # Time complexity is O(|V|log|V|) for a heap with a small graph
    # Time complexity is O(|V^2|log|V|) for a heap with a large graph
    # Space complexity is O(|V|)
    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        # Run Dijkstra's Algorithm
        # Time and space complexity are both O(|V|)
        # Go through each node in our network
        for current_node in self.network.nodes:
            # Check to see if the current node is the source node
            if current_node == self.network.nodes[self.source]:
                # If it is, set the index to the srcIndex and the distance to 0
                # The previous node is not known yet, so it is set to nil (None)
                self.node_dict.set_node(current_node, self.source, 0, None)
            # Otherwise, add the remaining nodes to the dictionary
            # The key is the current node, followed by the index, distance, and previous
            else:
                # We set the distance for each node to infinity
                # The node index and previous are not known yet, so we set them to nil
                self.node_dict.set_node(current_node, None, math.inf, None)

        # Check to see if we should use the heap or array implementation
        if use_heap:
            # Heap implementation has a time complexity of O(|V|log|V|)
            priority = PriorityHeap(self.network, self.node_dict)
        else:
            # Unsorted array implementation has a time complexity of O(|V|)
            priority = PriorityArray(self.network, self.node_dict)

        # While our priority queue is not empty O(|V|)
        while len(priority.queue) > 0:
            # Grab the current minimum node from our priority queue
            current_node = priority.delete_min()
            # Loop through each edge in the current node's neighbors
            for edge in current_node.neighbors:
                # Set our next node to the current edge's destination node
                next_node = edge.dest
                # Check to see if our next node's distance is greater than our current node's distance + edge length
                if self.node_dict[next_node][1] > (self.node_dict[current_node][1] + edge.length):
                    # If so, set the distance to our current node's distance + the edge length
                    distance = self.node_dict[current_node][1] + edge.length
                    # Grab the index so we don't overwrite it on the next line for the dictionary
                    next_index = self.node_dict[next_node][0]
                    # Update the next node with correct information in the dictionary
                    self.node_dict.set_node(next_node, next_index, distance, current_node)
                    # Decrease the key, time complexity is O(1) for the array and O(log|V|) for the heap
                    priority.decrease_key(next_node)

        t2 = time.time()
        return t2-t1
