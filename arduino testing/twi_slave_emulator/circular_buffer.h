////////////////////////////////////////////////////////////////////////////////////
//
//  circular_buffer.h
//
//  Written by Ethan Kessel (mailto:eqkessel@gmail.com).
//
//  Provides a polymorphic circular buffer class that allows for controlable
//  reading and writing to buffer objects. Both the datatype and length are
//  configurable at compile-time using templates. The class is also configurable
//  with an EOM detection system that will suppress the announcement of data
//  readiness until a specific EOM signal is recieved. This is particularly
//  useful with the Arduino's serial port since messages can be read from its
//  buffer faster than the baudrate resulting .available() becoming false before
//  an entire message is recieved. By instead buffering into this circular buffer
//  with the EOM signal set to '\n', the full message will be recieved before the
//  data in the buffer becomes available.
//
//  Data can be written into the buffer with write(), and may be done so until the
//  buffer is full (when the write head loops around to meet the read head), at
//  which point any data written into the buffer is dropped. write() returns the
//  number of data values written, so for the single value call it will return
//  either a 1 or 0.
//
//  Data that has been written to the buffer can be read with read(), and may be
//  done so until the read head catches up with the write head, at which point the
//  last value is returned for every subsequent read().
//
//  It is also possible to peek() into the data without performing a read. peek()
//  also allows the user to see data that has been buffered in but may not be
//  ready yet. peek() takes an optional argument signifying the number of indices
//  into the buffer to read, but cannot read past the write head and will return
//  last value before the write head in such a case.
//
//  It is possible to mark available values as read if you do not want to read all
//  of them with markRead(). This takes the number of values which you want to mark
//  as read as an argument. It will effectively move the read head forward as if
//  you had read the data without returning the data in the buffer that was skipped
//  over. This function cannot mark values that are not ready to be read as read,
//  and cannot pass the write head when marking values. This method returns the
//  number of values marked as read.
//
////////////////////////////////////////////////////////////////////////////////////
//
//  MIT License
//  
//  Copyright (c) 2020 Ethan Kessel
//  
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//  
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//  
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
////////////////////////////////////////////////////////////////////////////////////

#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H

template <typename type, size_t len>
class CircularBuffer
{
protected:
  type buffer_[len];
  size_t write_index_;
  size_t read_index_;
  size_t num_unread_;
  size_t num_ready_;
  bool use_eom_;
  type eom_signal_;

  size_t nextWriteIndex(void)
  {
    size_t nextIndex = write_index_ + 1;
    if (nextIndex >= len)
    {
      nextIndex = 0;
    }

    return(nextIndex);
  }

  size_t nextReadIndex(size_t num_indices = 1)
  {
    size_t nextIndex = read_index_ + num_indices;
    while (nextIndex >= len)
    {
      nextIndex -= len;
    }

    return(nextIndex);
  }

public:
  //  CONSTRUCTOR - DEFAULT
  CircularBuffer(void)
    : write_index_ (0)
    , read_index_ (0)
    , num_unread_ (0)
    , num_ready_ (0)
    , use_eom_ (false)
    , eom_signal_ (0)
  {
  }

  //  CONSTRUCTOR - EOM SIGNIFIER
  CircularBuffer(type eom)
    : write_index_ (0)
    , read_index_ (0)
    , num_unread_ (0)
    , num_ready_ (0)
    , use_eom_ (true)
    , eom_signal_ (eom)
  {
  }

  //  DESTRUCTOR
  ~CircularBuffer(void)
  {
  }

  size_t available(void)
  {
    return(num_ready_);
  }

  size_t numBuffered(void)
  {
    return(num_unread_);
  }

  size_t write(type data)
  {
    size_t n_vals = 0;
    if (num_unread_ < len)  // Write will not trample data that hasn't been read yet
    {
      buffer_[write_index_] = data;
      write_index_ = nextWriteIndex();
      ++n_vals;
      ++num_unread_;
    } // Otherwise pass and drop the data

    if (!use_eom_ || data == eom_signal_) // Update the number of ready-to-read values only if we are NOT using an eom signal or if the eom signal matches
    {
      num_ready_ = num_unread_;
    }

    return(n_vals); // Return the number of values written
  }

  size_t write(const type* data_array, size_t num_el)
  {
    size_t n_vals = 0;
    size_t last_write;
    
    if (data_array != NULL)
    {
      for (size_t i = 0; i < num_el; ++i)
      {
        last_write = write(data_array[i]);
        n_vals += last_write;

        if (last_write == 0)
        {
          break;  // Don't bother with remaining writes if we've already dropped something
        }
      }
    }

    return(n_vals); // Return the number of values written
  }

  type read(void)
  {
    type read_val = buffer_[read_index_];
    
    if (num_ready_ > 0)
    {
      read_index_ = nextReadIndex();
      --num_unread_;
      --num_ready_;
    }

    return(read_val);
  }

  type peek(size_t num_indices = 0)
  {
    size_t peek_index;
    
    if (num_indices > num_unread_)
    {
      peek_index = nextReadIndex(num_unread_);
    }
    else
    {
      peek_index = nextReadIndex(num_indices);
    }
    
    return(buffer_[peek_index]);
  }

  size_t markRead(size_t num_vals)
  {
    size_t num_to_mark;

    if (num_vals > num_ready_)
    {
      num_to_mark = num_ready_;
    }
    else
    {
      num_to_mark = num_vals;
    }

    read_index_ = nextReadIndex(num_to_mark);
    num_unread_ -= num_to_mark;
    num_ready_ -= num_to_mark;

    return(num_to_mark);
  }

  bool usesEOM(void)
  {
    return(use_eom_);
  }

  type eomSignal(void)
  {
    return(eom_signal_);
  }
  
};

#endif // CIRCULAR_BUFFER_H
